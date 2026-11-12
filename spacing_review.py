"""固定焦点最近邻距离的共享区域复核。"""
import numpy as np


class ReviewState:
    """只接收已知坐标、固定焦点和候选区域，不读取未返回的对象。"""
    def __init__(self, known, focal_ids, cells, scales=None):
        self.known = {str(k): np.asarray(v, dtype=float) for k, v in known.items()}
        if any(v.shape != (2,) or not np.isfinite(v).all() for v in self.known.values()):
            raise ValueError('已知坐标须为两个有限数值')
        self.focal_ids = [str(k) for k in focal_ids]
        if not self.focal_ids or not set(self.focal_ids) <= set(self.known):
            raise ValueError('焦点必须非空，且已包含在已知坐标中')
        if len(self.known) < 2:
            raise ValueError('至少需要两个已知对象')
        self.cells = np.asarray(cells, dtype=float)
        if not np.isfinite(self.cells).all() or self.cells.ndim != 2 or self.cells.shape[1] != 4 or np.any(self.cells[:,2:] <= self.cells[:,:2]):
            raise ValueError('候选区域须为有效的[x1,y1,x2,y2]矩形')
        self.focal_xy = np.asarray([self.known[k] for k in self.focal_ids])
        self.scales = np.ones(len(self.focal_ids)) if scales is None else np.asarray(scales,dtype=float)
        if not np.isfinite(self.scales).all() or self.scales.shape != (len(self.focal_ids),) or np.any(self.scales <= 0):
            raise ValueError('每个焦点须提供一个正的归一化尺度')
        delta = np.maximum(np.maximum(self.cells[None,:,:2]-self.focal_xy[:,None,:], self.focal_xy[:,None,:]-self.cells[None,:,2:]),0)
        self.cell_dist = np.linalg.norm(delta,axis=2)
        self.unread = np.ones(len(self.cells),dtype=bool)
        self.areas = np.prod(self.cells[:,2:]-self.cells[:,:2],axis=1)
        self.charged = 0.0
        self.tolerance = 1e-6

    def bounds(self):
        ids=list(self.known);xy=np.asarray([self.known[k] for k in ids])
        distance=np.linalg.norm(self.focal_xy[:,None,:]-xy[None,:,:],axis=2)
        distance[np.asarray(self.focal_ids)[:,None]==np.asarray(ids)[None,:]]=np.inf
        upper=distance.min(axis=1)
        lower=np.minimum(upper,self.cell_dist[:,self.unread].min(axis=1)) if self.unread.any() else upper.copy()
        return lower,upper

    def select(self, policy='distance', random_order=None):
        available=np.flatnonzero(self.unread)
        if not len(available):return None
        if policy=='random':
            if random_order is None:raise ValueError('随机策略需要预先生成的区域顺序')
            return next(int(i) for i in random_order if self.unread[i])
        if policy not in ('distance','nearest'):raise ValueError('未知策略')
        if policy=='distance':
            _,upper=self.bounds()
            score=(np.maximum(upper[:,None]-self.cell_dist[:,available],0)/self.scales[:,None]).sum(axis=0)
            if score.max()>1e-12:return int(available[np.argmax(score)])
        return int(available[np.argmin(self.cell_dist[:,available].min(axis=0))])

    def query(self, cell_id, return_centres, area_cap):
        """返回接口只接收当前选区；一次成功检查计费整个区域。"""
        i=int(cell_id)
        if not self.unread[i]:raise ValueError('该区域已复核')
        if self.charged+self.areas[i]>area_cap+1e-6:return False
        result=return_centres(self.cells[i].copy()); pending={}
        for k,v in result.items():
            xy=np.asarray(v,dtype=float)
            if xy.shape!=(2,) or not np.isfinite(xy).all():raise ValueError('返回坐标须为两个有限数值')
            x1,y1,x2,y2=self.cells[i]
            if not (x1<=xy[0]<x2 and y1<=xy[1]<y2):raise ValueError('返回对象不在选区半开边界内')
            if str(k) in self.known and not np.array_equal(self.known[str(k)],xy):raise ValueError('同一对象坐标发生变化')
            pending[str(k)]=xy
        self.known.update(pending)
        self.unread[i]=False;self.charged+=float(self.areas[i]);return True

    def confirmed(self):
        lower,upper=self.bounds()
        return bool(np.all(upper-lower<=self.tolerance))


def observable_focals(known, clearance):
    """以最近已知邻居和到覆盖边界的距离筛选，过程不需要未知对象坐标。"""
    ids=list(known)
    if len(ids)<2:return []
    xy=np.asarray([known[k] for k in ids],dtype=float)
    distances=np.linalg.norm(xy[:,None,:]-xy[None,:,:],axis=2)
    np.fill_diagonal(distances,np.inf)
    return [k for k,d in zip(ids,distances.min(axis=1)) if d<=clearance[k]+1e-6]

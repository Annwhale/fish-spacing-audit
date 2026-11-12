"""把JSON中的坐标替换为自己的坐标即可运行。"""
from pathlib import Path
import json
import numpy as np
from spacing_review import ReviewState,observable_focals

def run(path=None):
    path=Path(path) if path else Path(__file__).parent/'examples/coordinates.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    focal=observable_focals(data['known'],data['clearance'])
    state=ReviewState(data['known'],focal,data['cells'])
    # 实际应用中将此接口替换为人工复核或已验证的区域返回服务。
    def query(rect):
        x1,y1,x2,y2=rect
        return {k:v for k,v in data['reference'].items() if x1<=v[0]<x2 and y1<=v[1]<y2}
    while not state.confirmed():
        cell=state.select()
        if cell is None:break
        state.query(cell,query,float(state.areas.sum()))
    lo,hi=state.bounds()
    return {'fixed_focals':focal,'lower':lo.tolist(),'upper':hi.tolist(),'reviewed_area':state.charged,'candidate_area':float(state.areas.sum()),'fixed_focals_confirmed':state.confirmed(),'known_objects_at_stop':list(state.known),'complete_group_certified':False}

if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=True,indent=2))

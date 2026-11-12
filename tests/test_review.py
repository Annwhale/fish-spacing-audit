"""检查返回接口、预算、几何界以及两个停止终点的区别。"""
import unittest,json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from spacing_review import ReviewState,observable_focals
from example import run

class ReviewTests(unittest.TestCase):
    def test_fixed_stop_does_not_prove_complete_group(self):
        r=run();self.assertTrue(r['fixed_focals_confirmed']);self.assertNotIn('c',r['known_objects_at_stop']);self.assertEqual(r['upper'],[1.,1.])

    def test_indivisible_budget_and_shared_answer(self):
        state=ReviewState({'a':[0.,0.],'b':[4.,0.]},['a','b'],[[-1,-1,2,1],[2,-1,5,1]])
        calls=[]
        def answer(rect):calls.append(rect.tolist());return {'c':[1.,0.]}
        self.assertFalse(state.query(0,answer,5));self.assertFalse(calls)
        self.assertTrue(state.query(0,answer,6));self.assertEqual(state.charged,6)
        lo,hi=state.bounds();np.testing.assert_allclose(hi,[1,3]);self.assertTrue(np.all(lo<=hi))

    def test_query_rejects_outside_return(self):
        state=ReviewState({'a':[0.,0.],'b':[4.,0.]},['a'],[[-1,-1,2,1]])
        with self.assertRaises(ValueError):state.query(0,lambda _: {'x':[5.,0.]},6)

    def test_observable_admission_needs_no_hidden_objects(self):
        self.assertEqual(observable_focals({'a':[0,0],'b':[4,0]},{'a':3,'b':5}),['b'])

    def test_bounds_enclose_all_possible_return_positions(self):
        for x in [.2,.5,.9]:
            state=ReviewState({'a':[0.,0.],'b':[4.,0.]},['a','b'],[[0,-1,1,1],[1,-1,5,1]])
            lo,hi=state.bounds();truth=np.array([x,4-x]);self.assertTrue(np.all(lo<=truth));self.assertTrue(np.all(hi>=truth))

    def test_explicit_utf8_under_cp936_default(self):
        original=Path.open
        def changed(path,mode='r',buffering=-1,encoding=None,errors=None,newline=None):
            if 'b' not in mode and encoding is None:encoding='cp936'
            return original(path,mode,buffering,encoding,errors,newline)
        try:
            Path.open=changed;self.assertTrue(run()['fixed_focals_confirmed'])
        finally:Path.open=original

if __name__=='__main__':unittest.main()

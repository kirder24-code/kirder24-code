import unittest,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from acceptance_gate import read_csv,validate_mapping,validate_events,rollups,reconcile_reference_events,evaluate

class GateTests(unittest.TestCase):
    def setUp(self):
        self.mapping=read_csv(ROOT/'data'/'customer_tag_map.csv')
        self.events=read_csv(ROOT/'data'/'model_events.csv')
        self.refs=read_csv(ROOT/'data'/'reference_events.csv')
        self.contract=json.loads((ROOT/'canonical_event_contract.json').read_text())

    def test_sample_requires_human_review_due_to_unapproved_mapping(self):
        result=evaluate(ROOT)
        self.assertEqual(result['status'],'REVIEW')
        self.assertTrue(any('mapping_not_approved NS-03:PILOT_A' in x for x in result['review_reasons']))

    def test_all_confidences_are_separate_fields(self):
        for e in self.events:
            self.assertIn('detection_confidence',e)
            self.assertIn('causation_confidence',e)
            self.assertIn('quantification_confidence',e)

    def test_rollups_match_synthetic_values(self):
        facility,total=rollups(self.events)
        self.assertEqual(facility['NS-01'],2060.0)
        self.assertEqual(facility['NS-02'],1050.0)
        self.assertEqual(facility['NS-03'],710.0)
        self.assertEqual(total,3820.0)

    def test_reference_events_all_match(self):
        issues,matches=reconcile_reference_events(self.events,self.refs)
        self.assertFalse(issues)
        self.assertEqual(len(matches),5)

    def test_duplicate_event_rejected(self):
        bad=[dict(x) for x in self.events]+[dict(self.events[0])]
        reject,_=validate_events(bad,self.contract['required_fields'])
        self.assertTrue(any('duplicate_event_id' in x for x in reject))

    def test_invalid_volume_range_rejected(self):
        bad=[dict(x) for x in self.events]
        bad[0]['volume_low_m3']='1300'; bad[0]['volume_estimate_m3']='1240'
        reject,_=validate_events(bad,self.contract['required_fields'])
        self.assertTrue(any('invalid_volume_range' in x for x in reject))

    def test_confidence_out_of_bounds_is_review(self):
        bad=[dict(x) for x in self.events]
        bad[0]['causation_confidence']='1.2'
        _,review=validate_events(bad,self.contract['required_fields'])
        self.assertTrue(any('confidence_out_of_bounds' in x for x in review))

    def test_missing_provenance_rejected(self):
        bad=[dict(x) for x in self.events]
        bad[0]['provenance_id']=''
        reject,_=validate_events(bad,self.contract['required_fields'])
        self.assertTrue(any('missing_provenance_id' in x for x in reject))

    def test_mapping_unit_mismatch_without_transform_rejected(self):
        bad=[dict(x) for x in self.mapping]
        bad[4]['transform']='direct'
        reject,_=validate_mapping(bad)
        self.assertTrue(any('unit_transform_missing' in x for x in reject))

    def test_approving_pending_mapping_allows_accept(self):
        good=[dict(x) for x in self.mapping]
        good[-1]['status']='approved'
        reject,review=validate_mapping(good)
        self.assertFalse(reject)
        self.assertFalse(review)

if __name__=='__main__': unittest.main()

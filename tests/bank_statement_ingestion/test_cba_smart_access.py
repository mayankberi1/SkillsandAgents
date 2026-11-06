"""Date-column regression checks with synthetic PDF text positions."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).parents[2] / 'skills' / 'bank-statement-ingestion' / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import cba_smart_access as reader


class DateColumnTests(unittest.TestCase):
    def read(self, second_date='13 Feb', margin=True, last_amount='5,000.00'):
        def word(text, x, end, y):
            return f'<word xMin="{x}" xMax="{end}" yMin="{y}" yMax="{y+9}">{text}</word>'
        rows = [word(t, x, e, 10) for t, x, e in [
            ('Date',60,80), ('Transaction',91,140), ('Debit',350,380),
            ('Credit',420,450), ('Balance',500,540)]]
        for y, date, desc, amount, balance in [
            (30,'10 Feb','Shop','1,000.00','9,000.00'),
            (50,second_date,'IG.COM',last_amount,'4,000.00')]:
            if date:
                day, month = date.split()
                rows += [word(day,60,70,y),word(month,73,88,y)]
            rows += [word(desc,91,140,y),word(amount,340,380,y),word(balance,490,540,y)]
        if margin: rows.append(word('SL.R9.S955.D123.O',15,22,50.8))
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'statement.txt'
            p.write_text('Period 01 Feb 2026 - 28 Feb 2026\nAccount Number 00 0000 00000000\nOPENING BALANCE 10,000.00 CR\nCLOSING BALANCE 4,000.00 CR')
            p.with_suffix('.html').write_text('<html xmlns="http://www.w3.org/1999/xhtml"><page>'+''.join(rows)+'</page></html>')
            with patch.object(reader.subprocess,'run'):
                return reader.parse_text(p,Path(directory)/'statement.pdf')

    def test_margin_code_does_not_replace_date(self):
        result=self.read()
        self.assertEqual([r['date'] for r in result['records']],['2026-02-10','2026-02-13'])
        self.assertEqual(result['records'][1]['raw_date'],'13 Feb')
        self.assertEqual(result['records'][1]['amount'],-500000)
        self.assertIn('13 Feb',result['records'][1]['quote'])

    def test_missing_date_does_not_reuse_previous_transaction_date(self):
        with self.assertRaisesRegex(ValueError,'Missing transaction date'):
            self.read(second_date='')

    def test_unreadable_date_stops_extraction(self):
        with self.assertRaisesRegex(ValueError,'Unreadable date column'):
            self.read(second_date='xx Feb')

    def test_balance_mismatch_stops_extraction(self):
        with self.assertRaisesRegex(ValueError,'Running balance mismatch'):
            self.read(last_amount='4,999.00')

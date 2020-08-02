# NSE_EOD

## Installing on Linux

```
git clone 'https://github.com/opmashin/nse_eod'
cd nse_eod
python setup.py install
```

## Usage

```
import nse_eod
nse_eod.get_historical_data('ACC','01-01-2015','01-01-2020')
nse_eod.get_period_data('ACC','24month')
```



"""Observed elevation episode construction from user-supplied observations.

Extracted from the original research code; no laboratory records are included.
"""
import numpy as np
import pandas as pd
LEDGER_COLUMNS = ["episode_id", "compound", "last_low_date", "first_high_date", "first_observed_onset", "onset_interval_days", "peak_result", "end_date", "n_elevated_measurements", "MRL_at_onset", "method_unit_era", "Project", "SampleName", "timing_ambiguous", "right_censored", "censor_reason", "source_row_ids"]

def build_episodes(obs, gap=28, closure=1, start="2016-01-01"):
    o=obs[obs.date.ge(start)].copy().sort_values("date").reset_index(drop=True)
    current="UNKNOWN"; last_valid=None; last_low=None; active=None; lows=0
    ledger=[]; statuses=[]; unanchored=[]
    for r in o.to_dict("records"):
        date=r["date"]
        if last_valid is not None and (date-last_valid).days>gap:
            if active is not None:
                active["right_censored"]=True; active["censor_reason"]="continuity_gap"
            active=None; current="UNKNOWN"; last_low=None; lows=0
        s=r["state"]
        if s=="BELOW":
            if current=="ACTIVE":
                lows+=1
                if lows>=closure:
                    if active is not None:
                        active["end_date"]=date; active["right_censored"]=False; active["censor_reason"]=""
                    active=None; current="BELOW"; last_low=date
            else:
                current="BELOW"; last_low=date; lows=0
            last_valid=date
        elif s=="ELEVATED":
            lows=0
            if current=="BELOW" and last_low is not None:
                active={"episode_id": f"{r['compound']}_{date:%Y%m%d}", "compound":r["compound"], "last_low_date":last_low,"first_high_date":date,"first_observed_onset":date,"onset_interval_days":(date-last_low).days,"peak_result":r["numeric_max"],"end_date":pd.NaT,"n_elevated_measurements":1,"MRL_at_onset":r["mrl_ngL"],"method_unit_era":r["method_unit_era"],"Project":r["Project"],"SampleName":r["SampleName"],"timing_ambiguous":(date-last_low).days>1,"right_censored":True,"censor_reason":"end_of_archive","source_row_ids":r["source_row_ids"]}
                ledger.append(active)
            elif active is not None:
                active["n_elevated_measurements"]+=1
                active["peak_result"]=np.nanmax([active["peak_result"],r["numeric_max"]])
                active["source_row_ids"]+=";"+r["source_row_ids"]
            elif current != "ACTIVE":
                unanchored.append({"date":date,"compound":r["compound"],"reason":"high_without_continuous_prior_low","source_row_ids":r["source_row_ids"]})
            current="ACTIVE"; last_valid=date
        else:
            # Invalid assays never close an episode or become a low. They interrupt
            # known-low eligibility until a new classifiable result is observed.
            lows=0
            if current != "ACTIVE":
                current="UNKNOWN"; last_low=None
        statuses.append({"date":date,"observation_state":s,"state_after":current,"last_valid_date":last_valid,"last_low_date":last_low,"episode_id":active["episode_id"] if active else ""})
    return pd.DataFrame(ledger,columns=LEDGER_COLUMNS), pd.DataFrame(statuses), pd.DataFrame(unanchored,columns=["date","compound","reason","source_row_ids"])

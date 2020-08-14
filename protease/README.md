# SARS-CoV-2 main protease (apo, monomer) Folding@home simulations

| Bucket                                    | Prefix                           | Description                                                     |
|-------------------------------------------|----------------------------------|-----------------------------------------------------------------|
| fah-public-data-covid19-moonshot-dynamics | SARS-CoV-2_main_protease_monomer | Folding@home simulations of the SARS-CoV2 main protease monomer |


[Data on OSF](https://osf.io/d9tm2/wiki/home/)

## Upload instructions

In progress.

``` shell
$ python protease/list_trajectories_to_upload.py /data/chodera/rafal.wiewiora/protease/ > trajs
$ python upload_to_s3.py --profile fah-collaborator --bucket fah-public-data-covid19-moonshot-dynamics --key-prefix "SARS-CoV-2_main_protease_monomer" --strip-file-prefix "/data/chodera/rafal.wiewiora/protease/" $(cat trajs)
```



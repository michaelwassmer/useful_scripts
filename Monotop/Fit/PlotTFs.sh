variable=$1

rootplot rootplot_config.py had_templates_2018_TFs.root TF_ttbar_had_CR_ttbarEl_ttbar_had_SR_${variable} TF_ttbar_had_CR_ttbarMu_ttbar_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2018" --noclean --legend-entries='t#bar{t}_{CR(e)}/t#bar{t}_{SR},t#bar{t}_{CR(#mu)}/t#bar{t}_{SR}' --title="#bf{2018, 59.7fb^{-1} (13 TeV)}"
mv TFs_2018/plot.pdf TFs_2018/TFs_ttbar.pdf

rootplot rootplot_config.py had_templates_2018_TFs.root TF_wlnujets_had_CR_WEl_znunujets_had_SR_${variable} TF_wlnujets_had_CR_WMu_znunujets_had_SR_${variable} TF_wlnujets_had_SR_znunujets_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2018" --noclean --legend-entries='W_{CR(e)}/Z_{SR},W_{CR(#mu)}/Z_{SR},W_{SR}/Z_{SR}' --title="#bf{2018, 59.7fb^{-1} (13 TeV)}" --ymin=0.01
mv TFs_2018/plot.pdf TFs_2018/TFs_W.pdf

rootplot rootplot_config.py had_templates_2018_TFs.root TF_zlljets_had_CR_ZElEl_znunujets_had_SR_${variable} TF_zlljets_had_CR_ZMuMu_znunujets_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2018" --noclean --legend-entries='Z_{CR(e)}/Z_{SR},Z_{CR(#mu)}/Z_{SR}' --title="#bf{2018, 59.7fb^{-1} (13 TeV)}"
mv TFs_2018/plot.pdf TFs_2018/TFs_Z.pdf

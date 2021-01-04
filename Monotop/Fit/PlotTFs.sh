variable=$1

rootplot rootplot_config.py had_templates_2018_TFs.root TF_ttbar_had_CR_ttbarEl_ttbar_had_SR_${variable} TF_ttbar_had_CR_ttbarMu_ttbar_had_SR_${variable} TF_ttbar_had_CR_WEl_ttbar_had_SR_${variable} TF_ttbar_had_CR_WMu_ttbar_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2018" --noclean --legend-entries='t#bar{t}_{CR(t#bar{t}|e)}/t#bar{t}_{SR},t#bar{t}_{CR(t#bar{t}|#mu)}/t#bar{t}_{SR},t#bar{t}_{CR(W|e)}/t#bar{t}_{SR},t#bar{t}_{CR(W|#mu)}/t#bar{t}_{SR}' --title="#bf{2018, 59.7fb^{-1} (13 TeV)}"
mv TFs_2018/plot.pdf TFs_2018/TFs_ttbar.pdf

rootplot rootplot_config.py had_templates_2018_TFs.root TF_wlnujets_had_CR_WEl_znunujets_had_SR_${variable} TF_wlnujets_had_CR_WMu_znunujets_had_SR_${variable} TF_wlnujets_had_SR_znunujets_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2018" --noclean --legend-entries='W_{CR(W|e)}/Z_{SR},W_{CR(W|#mu)}/Z_{SR},W_{SR}/Z_{SR}' --title="#bf{2018, 59.7fb^{-1} (13 TeV)}" --ymin=0.01
mv TFs_2018/plot.pdf TFs_2018/TFs_W.pdf

rootplot rootplot_config.py had_templates_2018_TFs.root TF_zlljets_had_CR_ZElEl_znunujets_had_SR_${variable} TF_zlljets_had_CR_ZMuMu_znunujets_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2018" --noclean --legend-entries='Z_{CR(Z|ee)}/Z_{SR},Z_{CR(Z|#mu#mu)}/Z_{SR}' --title="#bf{2018, 59.7fb^{-1} (13 TeV)}"
mv TFs_2018/plot.pdf TFs_2018/TFs_Z.pdf

rootplot rootplot_config.py had_templates_2018_TFs.root TF_gammajets_had_CR_Gamma_znunujets_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2018" --noclean --legend-entries='#gamma_{CR(#gamma)}/Z_{SR}' --title="#bf{2018, 59.7fb^{-1} (13 TeV)}"
mv TFs_2018/TF_gammajets_had_CR_Gamma_znunujets_had_SR_${variable}.pdf TFs_2018/TFs_G.pdf



rootplot rootplot_config.py had_templates_2017_TFs.root TF_ttbar_had_CR_ttbarEl_ttbar_had_SR_${variable} TF_ttbar_had_CR_ttbarMu_ttbar_had_SR_${variable} TF_ttbar_had_CR_WEl_ttbar_had_SR_${variable} TF_ttbar_had_CR_WMu_ttbar_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2017" --noclean --legend-entries='t#bar{t}_{CR(t#bar{t}|e)}/t#bar{t}_{SR},t#bar{t}_{CR(t#bar{t}|#mu)}/t#bar{t}_{SR},t#bar{t}_{CR(W|e)}/t#bar{t}_{SR},t#bar{t}_{CR(W|#mu)}/t#bar{t}_{SR}' --title="#bf{2017, 41.5fb^{-1} (13 TeV)}"
mv TFs_2017/plot.pdf TFs_2017/TFs_ttbar.pdf

rootplot rootplot_config.py had_templates_2017_TFs.root TF_wlnujets_had_CR_WEl_znunujets_had_SR_${variable} TF_wlnujets_had_CR_WMu_znunujets_had_SR_${variable} TF_wlnujets_had_SR_znunujets_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2017" --noclean --legend-entries='W_{CR(W|e)}/Z_{SR},W_{CR(W|#mu)}/Z_{SR},W_{SR}/Z_{SR}' --title="#bf{2017, 41.5fb^{-1} (13 TeV)}" --ymin=0.01
mv TFs_2017/plot.pdf TFs_2017/TFs_W.pdf

rootplot rootplot_config.py had_templates_2017_TFs.root TF_zlljets_had_CR_ZElEl_znunujets_had_SR_${variable} TF_zlljets_had_CR_ZMuMu_znunujets_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2017" --noclean --legend-entries='Z_{CR(Z|ee)}/Z_{SR},Z_{CR(Z|#mu#mu)}/Z_{SR}' --title="#bf{2017, 41.5fb^{-1} (13 TeV)}"
mv TFs_2017/plot.pdf TFs_2017/TFs_Z.pdf

rootplot rootplot_config.py had_templates_2017_TFs.root TF_gammajets_had_CR_Gamma_znunujets_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2017" --noclean --legend-entries='#gamma_{CR(#gamma)}/Z_{SR}' --title="#bf{2017, 41.5fb^{-1} (13 TeV)}"
mv TFs_2017/TF_gammajets_had_CR_Gamma_znunujets_had_SR_${variable}.pdf TFs_2017/TFs_G.pdf



rootplot rootplot_config.py had_templates_2016_TFs.root TF_ttbar_had_CR_ttbarEl_ttbar_had_SR_${variable} TF_ttbar_had_CR_ttbarMu_ttbar_had_SR_${variable} TF_ttbar_had_CR_WEl_ttbar_had_SR_${variable} TF_ttbar_had_CR_WMu_ttbar_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2016" --noclean --legend-entries='t#bar{t}_{CR(t#bar{t}|e)}/t#bar{t}_{SR},t#bar{t}_{CR(t#bar{t}|#mu)}/t#bar{t}_{SR},t#bar{t}_{CR(W|e)}/t#bar{t}_{SR},t#bar{t}_{CR(W|#mu)}/t#bar{t}_{SR}' --title="#bf{2016, 35.9fb^{-1} (13 TeV)}"
mv TFs_2016/plot.pdf TFs_2016/TFs_ttbar.pdf

rootplot rootplot_config.py had_templates_2016_TFs.root TF_wlnujets_had_CR_WEl_znunujets_had_SR_${variable} TF_wlnujets_had_CR_WMu_znunujets_had_SR_${variable} TF_wlnujets_had_SR_znunujets_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2016" --noclean --legend-entries='W_{CR(W|e)}/Z_{SR},W_{CR(W|#mu)}/Z_{SR},W_{SR}/Z_{SR}' --title="#bf{2016, 35.9fb^{-1} (13 TeV)}" --ymin=0.01
mv TFs_2016/plot.pdf TFs_2016/TFs_W.pdf

rootplot rootplot_config.py had_templates_2016_TFs.root TF_zlljets_had_CR_ZElEl_znunujets_had_SR_${variable} TF_zlljets_had_CR_ZMuMu_znunujets_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2016" --noclean --legend-entries='Z_{CR(Z|ee)}/Z_{SR},Z_{CR(Z|#mu#mu)}/Z_{SR}' --title="#bf{2016, 35.9fb^{-1} (13 TeV)}"
mv TFs_2016/plot.pdf TFs_2016/TFs_Z.pdf

rootplot rootplot_config.py had_templates_2016_TFs.root TF_gammajets_had_CR_Gamma_znunujets_had_SR_${variable} --processors=1 --size=1024x768 --xlabel="#slash{U}_{T}[GeV]" --ylabel="Transfer factor" --legend-location='upper left' --gridx --gridy -e pdf --draw='histe' --output="TFs_2016" --noclean --legend-entries='#gamma_{CR(#gamma)}/Z_{SR}' --title="#bf{2016, 35.9fb^{-1} (13 TeV)}"
mv TFs_2016/TF_gammajets_had_CR_Gamma_znunujets_had_SR_${variable}.pdf TFs_2016/TFs_G.pdf

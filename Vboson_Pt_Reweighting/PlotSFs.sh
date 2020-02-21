# Z(ll) boson scale factors
rootplot rootplot_config.py 2018/TheoryXS_eej_madgraph_2018.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,l#bar{l}}" --ylabel="Scale factor" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="SFs_2018" --noclean
rootplot rootplot_config.py 2017/TheoryXS_eej_madgraph_2017.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,l#bar{l}}" --ylabel="Scale factor" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="SFs_2017" --noclean
rootplot rootplot_config.py 2016/TheoryXS_eej_madgraph_2016.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,l#bar{l}}" --ylabel="Scale factor" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="SFs_2016" --noclean

# Z(ll) boson theory cross sections
rootplot rootplot_config.py eej.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,l#bar{l}}" --ylabel="#sigma_{TH}" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="theory_xs" --noclean
rootplot rootplot_config.py eej.root --processors=6 --size=1024x768 --xlabel="p_{T,l#bar{l}}" --ylabel="#sigma_{TH}" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="theory_xs" --noclean --path='(?i).*k.*'

# Z(ll) boson mc cross sections
rootplot rootplot_config.py 2018/Zll_boson_pt_madgraph_2018.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,l#bar{l}}" --ylabel="#sigma_{MC}" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="mc_xs" --noclean

# W(lnu) boson scale factors
rootplot rootplot_config.py 2018/TheoryXS_evj_madgraph_2018.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,l#bar{#nu}_{l}}" --ylabel="Scale factor" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="SFs_2018" --noclean
rootplot rootplot_config.py 2017/TheoryXS_evj_madgraph_2017.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,l#bar{#nu}_{l}}" --ylabel="Scale factor" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="SFs_2017" --noclean
rootplot rootplot_config.py 2016/TheoryXS_evj_madgraph_2016.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,l#bar{#nu}_{l}}" --ylabel="Scale factor" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="SFs_2016" --noclean

# W(lnu) boson theory cross sections
rootplot rootplot_config.py evj.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,l#bar{#nu}_{l}}" --ylabel="#sigma_{TH}" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="theory_xs" --noclean
rootplot rootplot_config.py evj.root --processors=6 --size=1024x768 --xlabel="p_{T,l#bar{#nu}_{l}}" --ylabel="#sigma_{TH}" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="theory_xs" --noclean --path='(?i).*k.*'

# W(lnu) boson mc cross sections
rootplot rootplot_config.py 2018/W_boson_pt_madgraph_2018.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,l#bar{#nu}_{l}}" --ylabel="#sigma_{MC}" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="mc_xs" --noclean

# Z(nunu) boson scale factors
rootplot rootplot_config.py 2018/TheoryXS_vvj_madgraph_2018.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,#nu#bar{#nu}}" --ylabel="Scale factor" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="SFs_2018" --noclean
rootplot rootplot_config.py 2017/TheoryXS_vvj_madgraph_2017.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,#nu#bar{#nu}}" --ylabel="Scale factor" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="SFs_2017" --noclean
rootplot rootplot_config.py 2016/TheoryXS_vvj_madgraph_2016.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,#nu#bar{#nu}}" --ylabel="Scale factor" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="SFs_2016" --noclean

# Z(nunu) boson theory cross sections
rootplot rootplot_config.py vvj.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,#nu#bar{#nu}}" --ylabel="#sigma_{TH}" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="theory_xs" --noclean
rootplot rootplot_config.py vvj.root --processors=6 --size=1024x768 --xlabel="p_{T,#nu#bar{#nu}}" --ylabel="#sigma_{TH}" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="theory_xs" --noclean --path='(?i).*k.*'

# Z(nunu) boson mc cross sections
rootplot rootplot_config.py 2018/Zvv_boson_pt_madgraph_2018.root --processors=6 --size=1024x768 --logy --xlabel="p_{T,#nu#bar{#nu}}" --ylabel="#sigma_{MC}" --legend-location='None' --gridx --gridy --xmax=3000 -e pdf --draw='hist' --output="mc_xs" --noclean

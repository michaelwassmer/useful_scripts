// compile with: `root-config --cxx --cflags --evelibs` -Wall -o test.exe *.cpp `root-config --cflags --evelibs`

#include "HistoProducer.hpp"

int  main() {

HistoProducer test;
test.AddVariable("Evt_Pt_MET");
test.AddVariable("Neutralino_Pt");

return 0;

}

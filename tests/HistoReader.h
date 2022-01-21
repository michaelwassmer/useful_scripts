class HistoReader {
  public:
    HistoReader(std::string instance_label, std::string path_to_file, std::string histogram_name, bool bin_error, uint nthreads);
    ~HistoReader();
    float operator()(uint thread, float x);
    void UseEdgeBins(bool use_edge_bins);
  private:
    std::string instance_label_;
    std::string path_to_file_;
    std::string histogram_name_;
    bool bin_error_;
    uint nthreads_;

    std::vector<TH1D*> histos_;
    bool initialized_ = false;
    bool use_edge_bins_ = true;
};

HistoReader::HistoReader(std::string instance_label,
                         std::string path_to_file,
                         std::string histogram_name,
                         bool bin_error,
                         uint nthreads) : instance_label_{instance_label}, path_to_file_{path_to_file}, histogram_name_{histogram_name}, bin_error_{bin_error}, nthreads_{nthreads} {
    TFile* file = nullptr;
    TH1D*  histo = nullptr;
    if (path_to_file != "") { file = TFile::Open(path_to_file_.c_str(), "READ"); }
    else {
        std::cout << "HistoReader " << instance_label_ << ": no file given" << std::endl;
        throw std::exception();
    }
    if (file) {
        std::cout << "HistoReader " << instance_label_<< ": opened file " << path_to_file_ << std::endl;
        histo = (TH1D*)file->Get(histogram_name_.c_str());
        if (histo) {
            std::cout << "loaded histogram " << histogram_name_ << " from file " << path_to_file_ << std::endl;
            histo->SetDirectory(0);
            for(uint i=0;i<nthreads_;i++) {
                TH1D* clone = (TH1D*)histo->Clone();
                histos_.push_back(clone);
                histos_.back()->SetDirectory(0);
                std::cout << "created histogram clone " << histos_.back() << std::endl;
            }
            initialized_ = true;
        }
        else {
            std::cout << "HistoReader " << instance_label_<< ": scale factor histogram not found in file " << file << std::endl;
            throw std::exception();
        }
        file->Close();
    }
    else {
        std::cout << "HistoReader " << instance_label_<< ": scale factor file not read" << std::endl;
        throw std::exception();
    }
}

void HistoReader::UseEdgeBins(bool use_edge_bins) {
    use_edge_bins_ = use_edge_bins;
}

float HistoReader::operator()(uint thread, float x) {
    if (!initialized_) {
        std::cout << "HistoReader " << instance_label_<< ": not initiliazed" << std::endl;
        throw std::exception();
    }

    if(histos_.empty()) {
        std::cout << "HistoReader " << instance_label_<< ": no histograms found" << std::endl;
        throw std::exception();
    }

    if(thread > (histos_.size()-1)) {
        std::cout << "HistoReader " << instance_label_<< ": number of threads does not match the number of histograms" << std::endl;
        throw std::exception();
    }

    // std::cout << "x " << x << std::endl;

    int   bin = -1;
    float value = 0.;
    TH1D* histo = histos_.at(thread);
    // std::cout << "xmin " << histo->GetXaxis()->GetXmin() << std::endl;
    // std::cout << "xmax " << histo->GetXaxis()->GetXmax() << std::endl;
    
    if (use_edge_bins_) {
        x = std::max(float(x),float(histo->GetXaxis()->GetXmin()+0.001));
        x = std::min(float(x),float(histo->GetXaxis()->GetXmax()-0.001));
    }

    bool x_in_range = (x > histo->GetXaxis()->GetXmin()) && (x < histo->GetXaxis()->GetXmax());

    if (x_in_range) {
        bin = histo->FindBin(x);
        if (bin_error_) value = histo->GetBinError(bin);
        else value = histo->GetBinContent(bin);
    }
    // std::cout << "bin " << bin << std::endl;
    // std::cout << "value " << value << std::endl;

    return value;
}
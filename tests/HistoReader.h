#include <iostream>
#include <fmt/format.h>
#include <TFile.h>
#include <TH1D.h>
template <class T> class HistoReader
{
  public:
    HistoReader(std::string instance_label, std::string path_to_file, std::string histogram_name, bool use_bin_error,
                uint nthreads);
    ~HistoReader();
    float operator()(uint thread, T input);
    void UseEdgeBins(bool use_edge_bins);

  private:
    void PrintHistoInfo(TH1D *histo);
    std::string instance_label_;
    std::string path_to_file_;
    std::string histogram_name_;
    bool use_bin_error_;
    uint nthreads_;

    std::vector<TH1D *> histos_;
    bool initialized_ = false;
    bool use_edge_bins_ = true;
    std::string debug_string_;
};

template <class T> HistoReader<T>::~HistoReader()
{
}

template <class T>
HistoReader<T>::HistoReader(std::string instance_label, std::string path_to_file, std::string histogram_name,
                            bool use_bin_error, uint nthreads)
    : instance_label_{instance_label}, path_to_file_{path_to_file}, histogram_name_{histogram_name},
      use_bin_error_{use_bin_error}, nthreads_{nthreads}
{
    TFile *file = nullptr;
    TH1D *histo = nullptr;
    debug_string_ = fmt::format("HistoReader instance {}: ", instance_label_);
    std::cout << debug_string_ << "Starting initialization ..." << std::endl;
    if (path_to_file != "")
    {
        file = TFile::Open(path_to_file_.c_str(), "READ");
    }
    else
    {
        std::cout << debug_string_ << fmt::format("File to read was not given!") << std::endl;
        throw std::exception();
    }
    if (file)
    {
        std::cout << debug_string_ << fmt::format("Opened file {} succesfully.", path_to_file_) << std::endl;
        histo = (TH1D *)file->Get(histogram_name_.c_str());
        if (histo)
        {
            std::cout << debug_string_
                      << fmt::format("Loaded histogram {} from file {}.", histogram_name_, path_to_file_) << std::endl;
            histo->SetDirectory(0);
            std::cout << debug_string_ << "Giving some histogram information in the following." << std::endl;
            PrintHistoInfo(histo);
            std::cout << debug_string_
                      << fmt::format("Creating {} clones of histogram for implicit multithreading.", nthreads_)
                      << std::endl;
            for (uint i = 0; i < nthreads_; i++)
            {
                TH1D *clone = (TH1D *)histo->Clone();
                histos_.push_back(clone);
                histos_.back()->SetDirectory(0);
                std::cout << debug_string_
                          << fmt::format("Created histogram clone of {} ({}) in {}", histogram_name_, fmt::ptr(histo),
                                         fmt::ptr(histos_.back()))
                          << std::endl;
            }
        }
        else
        {
            std::cout << debug_string_
                      << fmt::format("Histogram {} not valid in file {}!", histogram_name_, path_to_file_) << std::endl;
            throw std::exception();
        }
        file->Close();
    }
    else
    {
        std::cout << debug_string_ << fmt::format("File {} not valid!", path_to_file_) << std::endl;
        throw std::exception();
    }
    initialized_ = true;
    std::cout << debug_string_ << "Finished initialization." << std::endl;
}

template <class T> void HistoReader<T>::PrintHistoInfo(TH1D *histo)
{
    std::cout << fmt::format("\t\t\t\t name: {}, title: {}", histo->GetName(), histo->GetTitle()) << std::endl;
    std::cout << fmt::format("\t\t\t\t # bins: {}, xmin: {}, xmax: {}", histo->GetNbinsX(),
                             histo->GetXaxis()->GetXmin(), histo->GetXaxis()->GetXmax())
              << std::endl;
    std::cout << fmt::format("\t\t\t\t entries: {}", histo->GetEntries()) << std::endl;
}

template <class T> void HistoReader<T>::UseEdgeBins(bool use_edge_bins)
{
    use_edge_bins_ = use_edge_bins;
}

template <class T> float HistoReader<T>::operator()(uint thread, T input)
{
    if (!initialized_)
    {
        std::cout << debug_string_ << fmt::format("Not initiliazed!") << std::endl;
        throw std::exception();
    }

    if (histos_.empty())
    {
        std::cout << debug_string_ << fmt::format("No available histograms found!") << std::endl;
        throw std::exception();
    }

    if (thread > (histos_.size() - 1))
    {
        std::cout << debug_string_
                  << fmt::format("Number/index of thread ({}) does not match the available number of histograms ({})!",
                                 thread, histos_.size())
                  << std::endl;
        throw std::exception();
    }

    // std::cout << "x " << x << std::endl;

    int bin = -1;
    float value = 0.;
    TH1D *histo = histos_.at(thread);
    // std::cout << "xmin " << histo->GetXaxis()->GetXmin() << std::endl;
    // std::cout << "xmax " << histo->GetXaxis()->GetXmax() << std::endl;
    float x = input;
    if (use_edge_bins_)
    {
        x = std::max(x, float(histo->GetXaxis()->GetXmin() + 0.001));
        x = std::min(x, float(histo->GetXaxis()->GetXmax() - 0.001));
    }

    bool x_in_range = (x > histo->GetXaxis()->GetXmin()) && (x < histo->GetXaxis()->GetXmax());

    if (x_in_range)
    {
        bin = histo->FindBin(x);
        if (use_bin_error_)
            value = histo->GetBinError(bin);
        else
            value = histo->GetBinContent(bin);
    }
    // std::cout << "bin " << bin << std::endl;
    // std::cout << "value " << value << std::endl;

    return value;
}

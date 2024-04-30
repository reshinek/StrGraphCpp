#include <pybind11/pybind11.h>
#include <iostream>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <vector>
#include <sstream>

namespace py = pybind11;
using namespace std;

class StrEngine
{
private:
    unordered_map<string, string> dict;

public:
    // constructor
    StrEngine()
    {
        dict = unordered_map<string, string>();
    }

    // return current string
    string setValue(const string &str1)
    {
        return str1;
    }

    // Concatenate two strings
    string concat(string &str1, const string &str2, const string &separator)
    {
        string newstr = str1 + separator + str2;
        // cout << newstr << endl;
        return newstr;
    }

    // duplicate string
    string duplicate(const string &str1, const string &separator)
    {
        string newstr = str1 + separator + str1;
        // cout << newstr << endl;
        return newstr;
    }

    // sort by letter
    string sortLetter(string &str)
    {
        sort(str.begin(), str.end());
        // cout << str << endl;
        return str;
    }

    // sort by word
    string sortWord(string &str)
    {
        std::istringstream iss(str);
        std::vector<std::string> words;
        std::string word;
        while (iss >> word)
        {
            words.push_back(word);
        }
        sort(words.begin(), words.end());
        string newstr = "";
        for (const std::string &word : words)
        {
            newstr += word;
        }
        return newstr;
    }

    // string to upper
    string toUpper(string &str)
    {
        transform(str.begin(), str.end(), str.begin(), ::toupper);
        // cout << str << endl;
        return str;
    }

    // string to lower
    string toLower(string &str)
    {
        transform(str.begin(), str.end(), str.begin(), ::tolower);
        // cout << str << endl;
        return str;
    }
};

PYBIND11_MODULE(StrEngine, m)
{
    m.doc() = "pybind11 engine plugin"; // optional module docstring

    py::class_<StrEngine>(m, "StrEngine")
        .def(py::init<>())
        .def("setValue", &StrEngine::setValue)
        .def("sortLetter", &StrEngine::sortLetter)
        .def("sortWord", &StrEngine::sortWord)
        .def("toUpper", &StrEngine::toUpper)
        .def("toLower", &StrEngine::toLower)
        .def("duplicate", &StrEngine::duplicate)
        .def("concat", &StrEngine::concat, py::arg("str1") = "", py::arg("str2") = "", py::arg("separator") = "");
}
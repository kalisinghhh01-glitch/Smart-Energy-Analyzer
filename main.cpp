
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>
#include <cstdlib>
using namespace std;

struct Appliance {
    string name;
    int quantity;
    double power;
    double hours;
};

const string DATA_FILE = "appliances.txt";

string clean(string s) {
    for (char &c : s)
        if (c == '|' || c == '\n' || c == '\r') c = ' ';
    return s;
}

vector<Appliance> loadData() {
    vector<Appliance> data;
    ifstream file(DATA_FILE);
    Appliance a;

    while (getline(file, a.name, '|')) {
        if (!(file >> a.quantity)) break;
        file.ignore();
        if (!(file >> a.power)) break;
        file.ignore();
        if (!(file >> a.hours)) break;
        file.ignore(10000, '\n');
        data.push_back(a);
    }
    return data;
}

void saveData(const vector<Appliance>& data) {
    ofstream file(DATA_FILE);
    for (const auto& a : data)
        file << clean(a.name) << "|" << a.quantity
             << "|" << a.power << "|" << a.hours << "\n";
}

double getEnergy(const Appliance& a) {
    return a.quantity * a.power * a.hours * 30 / 1000.0;
}

double getBill(double units) {
    if (units <= 100) return units * 3;
    if (units <= 200) return 300 + (units - 100) * 5;
    return 800 + (units - 200) * 7;
}

string escapeJSON(string s) {
    string result;
    for (char c : s) {
        if (c == '"' || c == '\\') result += '\\';
        if (c == '\n') {
            result += "\\n";
            continue;
        }
        if (c != '\r') result += c;
    }
    return result;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "{\"ok\":false,\"error\":\"Command missing\"}";
        return 1;
    }

    string command = argv[1];
    vector<Appliance> data = loadData();

    if (command == "list") {
        cout << "{\"ok\":true,\"appliances\":[";
        for (int i = 0; i < (int)data.size(); i++) {
            if (i) cout << ",";
            Appliance a = data[i];

            cout << "{\"name\":\"" << escapeJSON(a.name)
                 << "\",\"quantity\":" << a.quantity
                 << ",\"power\":" << a.power
                 << ",\"hours\":" << a.hours
                 << ",\"energy\":" << getEnergy(a) << "}";
        }
        cout << "]}";
    }

    else if (command == "add") {
        if (argc != 6) return 1;

        Appliance a;
        a.name = clean(argv[2]);
        a.quantity = atoi(argv[3]);
        a.power = atof(argv[4]);
        a.hours = atof(argv[5]);

        if (a.name.empty() || a.quantity <= 0 ||
            a.power <= 0 || a.hours <= 0 || a.hours > 24) {
            cout << "{\"ok\":false,\"error\":\"Invalid appliance details\"}";
            return 1;
        }

        data.push_back(a);
        saveData(data);
        cout << "{\"ok\":true,\"message\":\"Appliance added successfully\"}";
    }

    else if (command == "delete") {
        if (argc != 3) return 1;

        int index = atoi(argv[2]);
        if (index < 0 || index >= (int)data.size()) {
            cout << "{\"ok\":false,\"error\":\"Invalid index\"}";
            return 1;
        }

        data.erase(data.begin() + index);
        saveData(data);
        cout << "{\"ok\":true,\"message\":\"Appliance deleted\"}";
    }

    else if (command == "summary") {
        double total = 0, highest = 0;
        string highestName = "-";

        for (const auto& a : data) {
            double e = getEnergy(a);
            total += e;
            if (e > highest) {
                highest = e;
                highestName = a.name;
            }
        }

        string level = total < 100 ? "Low" :
                       total <= 300 ? "Medium" : "High";

        cout << fixed << setprecision(2);
        cout << "{\"ok\":true,\"total_units\":" << total
             << ",\"bill\":" << getBill(total)
             << ",\"level\":\"" << level
             << "\",\"highest_name\":\"" << escapeJSON(highestName)
             << "\",\"highest_energy\":" << highest << "}";
    }

    else if (command == "predict") {
        if (argc != 4) return 1;

        double previous = atof(argv[2]);
        double current = atof(argv[3]);

        if (previous < 0 || current < 0) {
            cout << "{\"ok\":false,\"error\":\"Invalid readings\"}";
            return 1;
        }

        double prediction = (previous + current) / 2;

        ofstream history("prediction_history.txt", ios::app);
        history << previous << "|" << current
                << "|" << prediction << "\n";

        cout << fixed << setprecision(2);
        cout << "{\"ok\":true,\"prediction\":" << prediction << "}";
    }

    else if (command == "report") {
        double total = 0;
        ofstream report("Energy_Report.txt");

        if (!report) {
            cout << "{\"ok\":false,\"error\":\"Report creation failed\"}";
            return 1;
        }

        report << fixed << setprecision(2);
        report << "SMART ENERGY ANALYZER REPORT\n";
        report << "============================\n\n";

        for (const auto& a : data) {
            double e = getEnergy(a);
            total += e;

            report << "Appliance: " << a.name << "\n";
            report << "Quantity: " << a.quantity << "\n";
            report << "Power: " << a.power << " W\n";
            report << "Daily Hours: " << a.hours << "\n";
            report << "Monthly Energy: " << e << " kWh\n\n";
        }

        report << "TOTAL ENERGY: " << total << " kWh\n";
        report << "ESTIMATED BILL: Rs. " << getBill(total) << "\n";
        report << "\nSample academic tariff, not actual utility rates.\n";

        report.close();
        cout << "{\"ok\":true,\"message\":\"Report generated successfully\"}";
    }

    else {
        cout << "{\"ok\":false,\"error\":\"Unknown command\"}";
        return 1;
    }

    return 0;
}

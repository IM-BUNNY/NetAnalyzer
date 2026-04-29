#include<iostream>
#include<map>
#include<vector>
#include<queue>
#include<string>
#include<limits>
#include<algorithm>
#include<set>
#include<sstream>
#include<cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

using namespace std;

// Trim whitespace from string
string trim(const string& str) {
    string s = str;
    s.erase(s.find_last_not_of(" \n\r\t") + 1);
    s.erase(0, s.find_first_not_of(" \n\r\t"));
    return s;
}

class Graph {
    map<string, vector<pair<string, double>>> adjList;
    set<string> validNodes;

public:
    void addEdge(const string& from, const string& to, double distance) {
        adjList[from].push_back({to, distance});
        adjList[to].push_back({from, distance});
        validNodes.insert(from);
        validNodes.insert(to);
    }

    pair<vector<string>, double> dijkstra(const string& start, const string& end) {
        if (validNodes.find(start) == validNodes.end() || validNodes.find(end) == validNodes.end()) {
            cout << "Invalid node: " << (validNodes.find(start) == validNodes.end() ? start : end) << endl;
            return {{}, -1};
        }

        map<string, double> dist;
        map<string, string> prev;
        priority_queue<pair<double, string>, vector<pair<double, string>>, greater<>> pq;

        for (const auto& node : adjList) {
            dist[node.first] = numeric_limits<double>::max();
        }
        dist[start] = 0;
        pq.push({0, start});

        while (!pq.empty()) {
            string u = pq.top().second;
            double d = pq.top().first;
            pq.pop();

            if (d > dist[u]) continue;

            for (const auto& neighbor : adjList[u]) {
                string v = neighbor.first;
                double weight = neighbor.second;

                if (dist[u] + weight < dist[v]) {
                    dist[v] = dist[u] + weight;
                    prev[v] = u;
                    pq.push({dist[v], v});
                }
            }
        }

        vector<string> path;
        if (dist[end] == numeric_limits<double>::max()) {
            cout << "No path exists between " << start << " and " << end << endl;
            return {path, -1};
        }

        string current = end;
        while (current != start) {
            path.push_back(current);
            current = prev[current];
        }
        path.push_back(start);
        reverse(path.begin(), path.end());

        cout << "Shortest path: ";
        for (size_t i = 0; i < path.size(); ++i) {
            cout << path[i];
            if (i < path.size() - 1) cout << " -> ";
        }
        cout << "\nTotal distance: " << dist[end] << " km" << endl;
        cout.flush();

        return {path, dist[end]};
    }
};

double haversineDistance(double lat1, double lon1, double lat2, double lon2) {
    const double R = 6371; // Earth's radius in km
    const double phi1 = lat1 * M_PI / 180;
    const double phi2 = lat2 * M_PI / 180;
    const double deltaPhi = (lat2 - lat1) * M_PI / 180;
    const double deltaLambda = (lon2 - lon1) * M_PI / 180;

    const double a = sin(deltaPhi/2) * sin(deltaPhi/2) +
                     cos(phi1) * cos(phi2) *
                     sin(deltaLambda/2) * sin(deltaLambda/2);
    const double c = 2 * atan2(sqrt(a), sqrt(1-a));

    return R * c;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    Graph g;

    vector<pair<string, pair<double, double>>> cities = {
        {"Shimla", {31.10483, 77.17339}},
        {"Manali", {32.2697, 77.1862}},
        {"Dharamshala", {32.2222, 76.3289}},
        {"Dalhousie", {32.5458, 76.0022}},
        {"Kasauli", {30.9167, 76.9667}},
        {"Solan", {30.9258, 77.0944}},
        {"Mandi", {31.7106, 76.9522}},
        {"Kullu", {31.9917, 77.1333}},
        {"Chamba", {32.5500, 76.1167}},
        {"Bilaspur", {31.3333, 76.7167}},
        {"Baddi", {30.9578, 76.7914}},
        {"Nalagarh", {31.0417, 76.7167}},
        {"Parwanoo", {30.8372, 76.9614}},
        {"Rampur", {31.4494, 77.6321}},
        {"Pooh", {31.7578, 78.5958}},
        {"Kaza", {32.2250, 78.0667}},
        {"Keylong", {32.5833, 77.0333}},
        {"Nurpur", {32.3000, 75.9000}},
        {"Jawalamukhi", {31.8746, 76.3191}},
        {"Kangra", {32.1000, 76.2667}},
        {"Palampur", {32.1167, 76.5333}},
        {"Baijnath", {32.0500, 76.6500}},
        {"Joginder Nagar", {31.9833, 76.7833}},
        {"Sundernagar", {31.5333, 76.9000}},
        {"Ghumarwin", {31.4333, 76.7167}},
        {"Kiratpur Sahib", {31.1833, 76.5667}},
        {"Aut", {31.9667, 77.2000}},
        {"Pandoh", {31.6667, 77.0500}}
    };

    vector<pair<string, string>> edges = {
        {"Parwanoo", "Solan"},
        {"Solan", "Shimla"},
        {"Shimla", "Rampur"},
        {"Rampur", "Pooh"},
        {"Pooh", "Kaza"},
        {"Kaza", "Manali"},
        {"Manali", "Keylong"},
        {"Baddi", "Nalagarh"},
        {"Nalagarh", "Kiratpur Sahib"},
        {"Kiratpur Sahib", "Bilaspur"},
        {"Bilaspur", "Ghumarwin"},
        {"Ghumarwin", "Sundernagar"},
        {"Sundernagar", "Mandi"},
        {"Mandi", "Pandoh"},
        {"Pandoh", "Aut"},
        {"Aut", "Kullu"},
        {"Kullu", "Manali"},
        {"Nurpur", "Jawalamukhi"},
        {"Jawalamukhi", "Kangra"},
        {"Kangra", "Dharamshala"},
        {"Dharamshala", "Palampur"},
        {"Palampur", "Baijnath"},
        {"Baijnath", "Joginder Nagar"},
        {"Joginder Nagar", "Mandi"},
        {"Dharamshala", "Dalhousie"},
        {"Dalhousie", "Chamba"},
        {"Solan", "Kasauli"}
    };

    map<string, pair<double, double>> cityCoords;
    for (const auto& city : cities) {
        cityCoords[city.first] = city.second;
    }

    for (const auto& edge : edges) {
        string from = edge.first;
        string to = edge.second;
        double lat1 = cityCoords[from].first;
        double lon1 = cityCoords[from].second;
        double lat2 = cityCoords[to].first;
        double lon2 = cityCoords[to].second;
        double distance = haversineDistance(lat1, lon1, lat2, lon2);
        g.addEdge(from, to, distance);
    }

    string start, end;
    getline(cin, start);
    getline(cin, end);

    start = trim(start);
    end = trim(end);

    if (start.empty() || end.empty()) {
        cerr << "Failed to read input: empty input" << endl;
        return 1;
    }

    auto result = g.dijkstra(start, end);
    if (result.second == -1) {
        return 1;
    }

    return 0;
}
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

/*
 Complex temp este O(nk), unde n este nr de elemente din sir si k e capacitatea
 Complex spat este O(nk) din cauza matricei dc
 Alg e de programare dinamica, cauta toate posibilitatile si stocheaza rez intermediare pt a evita calc redundant.
 Suma max <= k va fi optin, pt ca parcurge toate variantele si retine s max obt la fiecare etapa
 */
int knapsack(const vector<int>& s, int k)
{
    int n=s.size();

    //matrice dc de n+1 x k+1 pt calc capacitatii
    vector<vector<int>> dc(n+1, vector<int>(k+1,0));

    for (int i=1; i<=n; i++) {
        for (int j=1; j<=k; j++) {
            //el cur <= capacitate cur j
            if (s[i-1]<= j) {
                //s max cu sau fara el cur
                dc[i][j] = max(dc[i-1][j], dc[i-1][j-s[i-1]]+s[i-1]);
            } else {
                dc[i][j] = dc[i-1][j];
            }
        }
    }

    //s max dc[n][k]
    return dc[n][k];
}

int approximateKnapsack(vector<int>& S)
{

    //sort descresc
    sort(S.begin(), S.end(), greater<int>());

    int sFin=0;
    for (int i=0; i<S.size();i++) {
        sFin +=S[i];
    }

    int s=0;
    int i=0;
    while (s<=sFin/2 && i<S.size()) {
        s +=S[i];
        i++;
    }
    return s;
}


int main() {

    int k = 110;
    vector<int> s = {3, 4, 5, 15, 12, 45, 54};

    cout<<"Suma max <= "<<k << " este: " <<knapsack(s, k) <<endl;

    vector<int> S = {3, 4, 5, 15, 12, 45, 54};

    cout<<"S aprox = "<<approximateKnapsack(S) << endl;

    return 0;
}

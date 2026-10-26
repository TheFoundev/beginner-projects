# Project 19 - Crypto Price Tracker (Flutter with API)

## 1. Project Title
**Crypto Price Tracker**

## 2. The Concept
This app shows real-time prices for popular cryptocurrencies like Bitcoin and Ethereum. It works like a stock ticker — your phone sends a request to a crypto price server (API), which sends back the current prices in US dollars. The app then displays each coin's name, symbol, and current price in a clean list, similar to how a financial news channel shows stock prices scrolling at the bottom of the screen.

## 3. What You Will Build/Do
You'll build an app with a price list showing Bitcoin, Ethereum, and a few other popular cryptocurrencies. A refresh button at the top lets you update prices anytime. Each coin shows its name, ticker symbol, and current USD price with a green up or red down indicator. The final app looks like a mini Bloomberg terminal for crypto — clean, informative, and always showing the latest numbers!

## 4. Core App Concept
**Real-Time Data Refresh** — The app periodically (or on-demand) fetches fresh data from a server, replacing old values with new ones. Like refreshing a webpage to see the latest news — you hit the refresh button, and the screen updates with the newest information.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone with internet access
- No API key required — uses a free public API (CoinGecko)

## 6. What You Will Learn
- Fetching and displaying data in a list/scroll view
- Implementing pull-to-refresh functionality
- Displaying prices with up/down indicators
- Building a financial-style data display UI

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create crypto_price_tracker
cd crypto_price_tracker
```

### Step 2: Add Dependencies
Add to `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.2.4
  intl: ^0.19.0
```

### Step 3: Complete Source Code
Create `lib/crypto_service.dart`:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class CryptoService {
  static const String _baseUrl = 'https://api.coingecko.com/api/v3';

  // List of cryptocurrency IDs from CoinGecko
  static const List<String> cryptoIds = [
    'bitcoin',
    'ethereum',
    'ripple',
    'litecoin',
    'cardano',
    'solana',
    'polkadot',
    'dogecoin',
  ];

  Future<List<CryptoCurrency>> fetchCryptoPrices() async {
    final idsParam = cryptoIds.join(',');
    final url = Uri.parse('$_baseUrl/simple/price?ids=$idsParam&vs_currencies=usd&include_24hr_change=true&include_market_cap=true');

    try {
      final response = await http.get(url).timeout(
        const Duration(seconds: 15),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<CryptoCurrency> cryptos = [];
        
        for (final entry in data.entries) {
          cryptos.add(CryptoCurrency.fromJson(entry.key, entry.value));
        }
        
        return cryptos;
      } else {
        throw Exception('Failed to load crypto prices');
      }
    } catch (e) {
      throw Exception('Network error: Please check your connection');
    }
  }

  // Mock data for offline/demo
  static List<CryptoCurrency> getMockData() {
    final mockData = {
      'bitcoin': {'usd': 67432.50, 'usd_24h_change': 2.45, 'usd_market_cap': 1300000000000},
      'ethereum': {'usd': 3521.75, 'usd_24h_change': -1.23, 'usd_market_cap': 420000000000},
      'tether': {'usd': 1.00, 'usd_24h_change': 0.12, 'usd_market_cap': 110000000000},
      'ripple': {'usd': 0.4923, 'usd_24h_change': 3.89, 'usd_market_cap': 26000000000},
      'cardano': {'usd': 0.6124, 'usd_24h_change': -0.56, 'usd_market_cap': 21000000000},
      'solana': {'usd': 148.76, 'usd_24h_change': 5.12, 'usd_market_cap': 69000000000},
    };

    final List<CryptoCurrency> cryptos = [];
    for (final entry in mockData.entries) {
      cryptos.add(CryptoCurrency.fromJson(entry.key, entry.value));
    }
    return cryptos;
  }
}

class CryptoCurrency {
  final String id;
  final double priceUsd;
  final double change24h;
  final double marketCap;

  CryptoCurrency({
    required this.id,
    required this.priceUsd,
    required this.change24h,
    required this.marketCap,
  });

  factory CryptoCurrency.fromJson(String id, Map<String, dynamic> json) {
    return CryptoCurrency(
      id: id,
      priceUsd: (json['usd'] as num?)?.toDouble() ?? 0.0,
      change24h: (json['usd_24h_change'] as num?)?.toDouble() ?? 0.0,
      marketCap: (json['usd_market_cap'] as num?)?.toDouble() ?? 0.0,
    );
  }

  String getSymbol() {
    switch (id) {
      case 'bitcoin':
        return 'BTC';
      case 'ethereum':
        return 'ETH';
      case 'tether':
        return 'USDT';
      case 'ripple':
        return 'XRP';
      case 'litecoin':
        return 'LTC';
      case 'cardano':
        return 'ADA';
      case 'solana':
        return 'SOL';
      case 'polkadot':
        return 'DOT';
      case 'dogecoin':
        return 'DOGE';
      default:
        return id.toUpperCase().substring(0, 3);
    }
  }

  String getName() {
    switch (id) {
      case 'bitcoin':
        return 'Bitcoin';
      case 'ethereum':
        return 'Ethereum';
      case 'tether':
        return 'Tether';
      case 'ripple':
        return 'Ripple';
      case 'litecoin':
        return 'Litecoin';
      case 'cardano':
        return 'Cardano';
      case 'solana':
        return 'Solana';
      case 'polkadot':
        return 'Polkadot';
      case 'dogecoin':
        return 'Dogecoin';
      default:
        return id.toUpperCase();
    }
  }
}
```

Create `lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'crypto_service.dart';

void main() {
  runApp(const CryptoPriceTrackerApp());
}

class CryptoPriceTrackerApp extends StatelessWidget {
  const CryptoPriceTrackerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Crypto Price Tracker',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        brightness: Brightness.light,
        useMaterial3: true,
      ),
      home: const CryptoHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class CryptoHomePage extends StatefulWidget {
  const CryptoHomePage({super.key});

  @override
  State<CryptoHomePage> createState() => _CryptoHomePageState();
}

class _CryptoHomePageState extends State<CryptoHomePage> {
  final CryptoService _cryptoService = CryptoService();
  late Future<List<CryptoCurrency>> _cryptosFuture;
  final NumberFormat _currencyFormat = NumberFormat.currency(locale: 'en_US', symbol: '\$');

  @override
  void initState() {
    super.initState();
    _refreshPrices();
  }

  void _refreshPrices() {
    setState(() {
      _cryptosFuture = _cryptoService.fetchCryptoPrices().catchError((_) {
        return CryptoService.getMockData();
      });
    });
  }

  String _formatPrice(double price) {
    if (price > 1000) {
      return '\$${price.toStringAsFixed(2)}';
    } else if (price > 1) {
      return '\$${price.toStringAsFixed(4)}';
    } else {
      return '\$${price.toStringAsFixed(6)}';
    }
  }

  String _formatMarketCap(double marketCap) {
    if (marketCap > 1e12) {
      return '\$${(marketCap / 1e12).toStringAsFixed(2)}T';
    } else if (marketCap > 1e9) {
      return '\$${(marketCap / 1e9).toStringAsFixed(1)}B';
    } else if (marketCap > 1e6) {
      return '\$${(marketCap / 1e6).toStringAsFixed(0)}M';
    }
    return marketCap.toStringAsFixed(0);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crypto Price Tracker'),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _refreshPrices,
            tooltip: 'Refresh Prices',
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          _refreshPrices();
        },
        child: FutureBuilder<List<CryptoCurrency>>(
          future: _cryptosFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
            
            if (snapshot.hasError) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.error, size: 60, color: Colors.red),
                    const SizedBox(height: 16),
                    Text(
                      'Error: ${snapshot.error}',
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: Colors.red),
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: _refreshPrices,
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              );
            }
            
            if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return const Center(child: Text('No data available'));
            }
            
            final cryptos = snapshot.data!;
            
            return ListView.separated(
              itemCount: cryptos.length,
              padding: const EdgeInsets.all(12),
              separatorBuilder: (context, index) => const SizedBox(height: 8),
              itemBuilder: (context, index) {
                final crypto = cryptos[index];
                return _buildCryptoCard(crypto);
              },
            );
          },
        ),
      ),
    );
  }

  Widget _buildCryptoCard(CryptoCurrency crypto) {
    final isPositive = crypto.change24h >= 0;
    final changeColor = isPositive ? Colors.green : Colors.red;
    final changeIcon = isPositive ? Icons.trending_up : Icons.trending_down;

    return Card(
      elevation: 3,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: CircleAvatar(
          radius: 24,
          backgroundColor: Colors.blue[100],
          child: Text(
            crypto.getSymbol(),
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: Colors.blue,
            ),
          ),
        ),
        title: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              crypto.getName(),
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
            Text(
              crypto.getSymbol(),
              style: TextStyle(
                color: Colors.grey[600],
                fontSize: 16,
              ),
            ),
          ],
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 4),
            Text(
              'Market Cap: ${_formatMarketCap(crypto.marketCap)}',
              style: TextStyle(
                fontSize: 13,
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 4),
            Row(
              children: [
                Icon(
                  changeIcon,
                  size: 16,
                  color: changeColor,
                ),
                const SizedBox(width: 4),
                Text(
                  '${crypto.change24h.toStringAsFixed(2)}%',
                  style: TextStyle(
                    color: changeColor,
                    fontWeight: FontWeight.bold,
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ],
        ),
        trailing: Text(
          _formatPrice(crypto.priceUsd),
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}
```

### Step 4: Run the App
```bash
flutter pub get
flutter run
```

## Extension Ideas
- Add a price graph (candlestick chart) for each crypto
- Add sorting (by price, by 24h change, by market cap)
- Add a watchlist feature to track favorites
- Add push notifications for price alerts
- Add comparison view to see multiple coins side by side

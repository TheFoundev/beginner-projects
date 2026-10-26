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
    final url = Uri.parse(
        '$_baseUrl/simple/price?ids=$idsParam&vs_currencies=usd&include_24hr_change=true&include_market_cap=true');

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
      throw Exception('Network error: $e');
    }
  }

  // Mock data for when API is unavailable
  static List<CryptoCurrency> getMockData() {
    final mockData = {
      'bitcoin': {
        'usd': 67432.50,
        'usd_24h_change': 2.45,
        'usd_market_cap': 1300000000000.0,
      },
      'ethereum': {
        'usd': 3521.75,
        'usd_24h_change': -1.23,
        'usd_market_cap': 420000000000.0,
      },
      'ripple': {
        'usd': 0.4923,
        'usd_24h_change': 3.89,
        'usd_market_cap': 26000000000.0,
      },
      'cardano': {
        'usd': 0.6124,
        'usd_24h_change': -0.56,
        'usd_market_cap': 21000000000.0,
      },
      'solana': {
        'usd': 148.76,
        'usd_24h_change': 5.12,
        'usd_market_cap': 69000000000.0,
      },
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
      priceUsd: (json['usd'] as num).toDouble(),
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

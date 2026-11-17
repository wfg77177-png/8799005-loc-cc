import SwiftUI
import WebKit

struct ContentView: View {
    var body: some View {
        WebView()
            .ignoresSafeArea()
    }
}

struct WebView: UIViewRepresentable {
    // 先走 https；证书还没下来时 https 会失败，自动退回 http
    private static let httpsURL = URL(string: "https://8799005.loc.cc/")!
    private static let httpURL = URL(string: "http://8799005.loc.cc/")!

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []
        let webView = WKWebView(frame: .zero, configuration: config)
        webView.navigationDelegate = context.coordinator
        webView.allowsBackForwardNavigationGestures = true
        webView.scrollView.bounces = true
        webView.load(URLRequest(url: Self.httpsURL))
        return webView
    }

    func updateUIView(_ webView: WKWebView, context: Context) {}

    class Coordinator: NSObject, WKNavigationDelegate {
        private var triedHttpFallback = false

        func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
            // https 失败（证书未就绪等）时退回 http 再试一次
            if !triedHttpFallback {
                triedHttpFallback = true
                webView.load(URLRequest(url: WebView.httpURL))
            }
        }

        func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
            if !triedHttpFallback {
                triedHttpFallback = true
                webView.load(URLRequest(url: WebView.httpURL))
            }
        }
    }
}

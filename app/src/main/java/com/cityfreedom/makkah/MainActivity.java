package com.cityfreedom.makkah;
import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebSettings;
public class MainActivity extends Activity {
 private WebView web;
 @Override public void onCreate(Bundle state) { super.onCreate(state);
  getWindow().getDecorView().setSystemUiVisibility(5894 | View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);
  web = new WebView(this); web.setFocusable(true); web.setFocusableInTouchMode(true); setContentView(web);
  WebSettings s=web.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true); s.setMediaPlaybackRequiresUserGesture(false); s.setAllowFileAccess(false);
  web.setWebChromeClient(new WebChromeClient()); web.setWebViewClient(new WebViewClient());
  web.loadUrl("https://papaya-biscochitos-8775bb.netlify.app/"); web.requestFocus();
 }
 @Override public void onBackPressed(){ if(web.canGoBack())web.goBack(); else super.onBackPressed(); }
 @Override public void onDestroy(){ web.destroy(); super.onDestroy(); }
}
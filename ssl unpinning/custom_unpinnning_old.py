import frida, sys


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)



jscode = """
    setTimeout(function() {
        Java.perform(function() {
            console.log("");
            console.log("[.] Android Cert Pinning Bypass");

            var CertificateFactory = Java.use("java.security.cert.CertificateFactory");
            var FileInputStream = Java.use("java.io.FileInputStream");
            var BufferedInputStream = Java.use("java.io.BufferedInputStream");
            var X509Certificate = Java.use("java.security.cert.X509Certificate");
            var KeyStore = Java.use("java.security.KeyStore");
            var TrustManagerFactory = Java.use("javax.net.ssl.TrustManagerFactory");
            var SSLContext = Java.use("javax.net.ssl.SSLContext");
            var X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
            //var is_android_n = 0;

            //--------
            console.log("[.] TrustManagerImpl Android 7+ detection...");
            // Android 7+ TrustManagerImpl
            // The work in the following NCC blogpost was a great help for this hook!
            // hattip @AdriVillaB :)
            // https://www.nccgroup.trust/uk/about-us/newsroom-and-events/blogs/2017/november/bypassing-androids-network-security-configuration/
            try {
                var TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');
                // https://github.com/google/conscrypt/blob/c88f9f55a523f128f0e4dace76a34724bfa1e88c/platform/src/main/java/org/conscrypt/TrustManagerImpl.java#L650
                TrustManagerImpl.verifyChain.implementation = function(untrustedChain, trustAnchorChain, host, clientAuth, ocspData, tlsSctData) {
                    console.log("[+] (Android 7+) TrustManagerImpl verifyChain() called. Not throwing an exception.");
                    // Skip all the logic and just return the chain again :P
                    //is_android_n = 1;
                    return untrustedChain;
                }

                PinningTrustManager.checkServerTrusted.implementation = function() {
                    console.log("[+] Appcelerator checkServerTrusted() called. Not throwing an exception.");
                }
            } catch (err) {
                console.log("[-] TrustManagerImpl Not Found");
            }

            //if (is_android_n === 0) {
            //--------
            console.log("[.] TrustManager Android < 7 detection...");
            // Implement a new TrustManager
            // ref: https://gist.github.com/oleavr/3ca67a173ff7d207c6b8c3b0ca65a9d8
            var TrustManager = Java.registerClass({
                name: 'com.sensepost.test.TrustManager',
                implements: [X509TrustManager],
                methods: {
                    checkClientTrusted: function(chain, authType) {},
                    checkServerTrusted: function(chain, authType) {},
                    getAcceptedIssuers: function() {
                        return [];
                    }
                }
            }); 

            // Prepare the TrustManagers array to pass to SSLContext.init()
            var TrustManagers = [TrustManager.$new()];

            // Get a handle on the init() on the SSLContext class
            var SSLContext_init = SSLContext.init.overload(
                '[Ljavax.net.ssl.KeyManager;', '[Ljavax.net.ssl.TrustManager;', 'java.security.SecureRandom');

            try {
                // Override the init method, specifying our new TrustManager
                SSLContext_init.implementation = function(keyManager, trustManager, secureRandom) {
                    console.log("[+] Overriding SSLContext.init() with the custom TrustManager android < 7");
                    SSLContext_init.call(this, keyManager, TrustManagers, secureRandom);
                };
            } catch (err) {
                console.log("[-] TrustManager Not Found");
            }
            //}

            //-------
            console.log("[.] OkHTTP 3.x detection...");
            // OkHTTP v3.x
            // Wrap the logic in a try/catch as not all applications will have
            // okhttp as part of the app.
            try {
                var CertificatePinner = Java.use('okhttp3.CertificatePinner');
                console.log("[+] OkHTTP 3.x Found");
                CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function() {
                    console.log("[+] OkHTTP 3.x check() called. Not throwing an exception.");
                };
            } catch (err) {
                // If we dont have a ClassNotFoundException exception, raise the
                // problem encountered.
                console.log("[-] OkHTTP 3.x Not Found")
            }

            //--------
            console.log("[.] Appcelerator Titanium detection...");
            // Appcelerator Titanium PinningTrustManager
            // Wrap the logic in a try/catch as not all applications will have
            // appcelerator as part of the app.
            try {
                var PinningTrustManager = Java.use('appcelerator.https.PinningTrustManager');
                console.log("[+] Appcelerator Titanium Found");
                PinningTrustManager.checkServerTrusted.implementation = function() {
                    console.log("[+] Appcelerator checkServerTrusted() called. Not throwing an exception.");
                }

            } catch (err) {
                // If we dont have a ClassNotFoundException exception, raise the
                // problem encountered.
                console.log("[-] Appcelerator Titanium Not Found");
            }
            try {
                     //okhttp
                        var OpenSSLSocketImpl = Java.use("com.android.org.conscrypt.OpenSSLSocketImpl")
                
                        OpenSSLSocketImpl.verifyCertificateChain.implementation = function(certRefs, authMethod){
                            console.log("verifyCertificateChain() hooked")
                            //do nothing
                            return true;
                        }
                    
             

            } catch (err) {
                     console.log("[-] OpenSSLSocketImpl Not Found");
            }
            
             try {
                        // Invalidate the certificate pinner set up
                    var OkHttpClient = Java.use("com.squareup.okhttp.OkHttpClient");
                    OkHttpClient.setCertificatePinner.implementation = function(certificatePinner){
                        // do nothing
                        console.log("Called!");
                        return this;
                    };
                
                    // Invalidate the certificate pinnet checks (if "setCertificatePinner" was called before the previous invalidation)
                    var CertificatePinner = Java.use("com.squareup.okhttp.CertificatePinner");
                    CertificatePinner.check.overload('java.lang.String', '[Ljava.security.cert.Certificate;').implementation = function(p0, p1){
                        // do nothing
                        console.log("Called! [Certificate]");
                        return;
                    };
                    CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function(p0, p1){
                        // do nothing
                        console.log("Called! [List]");
                        return;
                    };
                } catch (err) {
                     console.log("[-] com.squareup.okhttp.OkHttpClient Not Found");
            }
             // Trustkit
            try {
                var Activity = Java.use("com.datatheorem.android.trustkit.pinning.OkHostnameVerifier");
                Activity.verify.overload('java.lang.String', 'javax.net.ssl.SSLSession').implementation = function (str) {
                    console.log('[+] Intercepted Trustkit{1}: ' + str);
                    return true;
                };
                Activity.verify.overload('java.lang.String', 'java.security.cert.X509Certificate').implementation = function (str) {
                    console.log('[+] Intercepted Trustkit{2}: ' + str);
                    return true;
                };
        
                console.log('[+] Setup Trustkit pinning')
            } catch(err) {
                console.log('[-] Trustkit pinner not found')
            }

        });
    }, 0);
"""

rdev=None
try:

    rdev = frida.get_usb_device()
except Exception ,e:
    print e

try:

    rdev = frida.get_remote_device()
except Exception, e:
    print e
front_app = rdev.get_frontmost_application()
print (front_app)
process = frida.get_usb_device().attach(front_app.identifier)
script = process.create_script(jscode)
script.load()
sys.stdin.read()

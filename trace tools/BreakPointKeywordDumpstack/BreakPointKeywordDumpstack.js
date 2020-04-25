setImmediate(function() {
	
    Java.perform(function (){
		
    	console.log("enter hook");          
		 // Create an instance of java.lang.String and initialize it with a string.
        const JavaString = Java.use('java.lang.String');
        var exampleString1 = JavaString.$new('Hello World, this is an example string in Java.');

        // Create an instance of java.nio.charset.Charset, and initialize the default character set.
        const Charset = Java.use('java.nio.charset.Charset');
        var charset = Charset.defaultCharset();
        
        // Create an instance of java.lang.String and initialize it through an overloaded $new, 
        // with a byte array and a instance of java.nio.charset.Charset.
        JavaString.$init.overload('[B', 'java.nio.charset.Charset').implementation=function(chars, charseta){
			var JString = Java.use('java.lang.String');
			var str = JString.$new(Java.array('byte', chars));
			console.log("JavaString.$init.overload('[B', 'java.nio.charset.Charset')=>"+str.toString());
			return this.$init(chars, charseta);
			
		}
	  JavaString.$init.overload('[B').implementation=function(chars){
			var JString = Java.use('java.lang.String');
			var str = JString.$new(Java.array('byte', chars));
			onsole.log("JavaString.$init.overload('[B')=>"+str.toString());
			return this.$init(chars);
		}

        // Intercept the initialization of java.lang.Stringbuilder's overloaded constructor.
        // Write the partial argument to the console.
        const StringBuilder = Java.use('java.lang.StringBuilder');
        //We need to overwrite .$init() instead of .$new(), since .$new() = .alloc() + .init()
        StringBuilder.$init.overload('java.lang.String').implementation = function (arg) {
            var partial = "";
            var result = this.$init(arg);
            /*if (arg !== null) {
                partial = arg.toString().replace('\n', '').slice(0,10);
            }*/
            // console.log('new StringBuilder(java.lang.String); => ' + result)
            console.log('new StringBuilder("")' + result.toString() )
            return result;
        }
        console.log('[+] new StringBuilder(java.lang.String) hooked');

        // Intercept the toString() method of java.lang.StringBuilder and write its partial contents to the console.        
        StringBuilder.toString.implementation = function () {
            var result = this.toString();
			/*
            var partial = "";
            if (result !== null) {
                partial = result.toString().replace('\n', '').slice(0,10);
            }*/
			
			/*
				Line 8556: StringBuilder.toString(); => GET http://789.kakamobi.cn/api/open/v3/advert-sdk/get.htm?_platform=android&_srv=t&_appName=jiakaobaodian&_product=%E9%A9%BE%E8%80%83%E5%AE%9D%E5%85%B8&_vendor=baidu&_renyuan=XYX&_version=7.2.6&_system=N2G47H&_manufacturer=Xiaomi&_systemVersion=7.1.2&_device=Redmi%205A&_imei=869288034063025&_productCategory=jiakaobaodian&_operator=&_androidId=fdaa05b5a62352a&_mac=d8%3A32%3Ae3%3Aa5%3A7c%3A97&_appUser=83bab26ad9e14c23a5a976dbbc7da548&_pkgName=com.handsgo.jiakao.android&_screenDpi=2.0&_screenWidth=720&_screenHeight=1280&_network=wifi&_launch=6&_firstTime=2019-01-23%2015%3A32%3A03&_apiLevel=25&_userCity=330100&_p=&_gpsType=gcj&_cityName=%E6%9D%AD%E5%B7%9E%E5%B8%82&_cityCode=330100&_gpsCity=330100&_longitude=120.16608&_latitude=30.185438&_ipCity=330100&_j=1.0&schoolName=%E8%90%A7%E5%B1%B1%E9%A9%BE%E6%A0%A1&schoolCode=330100380&_webviewVersion=4.7&_mcProtocol=4.1&adver=4&adStatus=1548314989980&_r=e3166f66ca7c4d06be5cd5f039c6e1d5&adid=85&sign=a0d58c790ad273acc2f31361414...
	Li
		   search keywords and throw exception
		   这里修改需要打印追中调用的参数名
			*/
			if (result.indexOf("sign")!=-1){
				console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()))
			}
			//blacklist
			var temp=result.toString();
			var arr = [" planTime="," dispatchTime="," finishTime=","{ when=","Rect(","draw Rect"];
			var match=false;
			for ( var i = 0; i <arr.length; i++){
				if(temp.startsWith(arr[i])){
					match=true;
					break;
				}
				
			
			}
			if(!match){
				console.log('StringBuilder.toString(); => ' + temp)
			}else{
				//console.log("blacklist");
			}
			return result;
			
        }
        console.log('[+] StringBuilder.toString() hooked');
			
		
	});
	 
       
    
	
	
});
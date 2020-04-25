function getGenericInterceptor(className, func, parameters) {
	args = []
	for (i = 0; i < parameters.length; i++) { 
        	args.push('arg_' + i) 
    }
    var script = "result = this.__FUNCNAME__(__SEPARATED_ARG_NAMES__);\nlogmessage = '__CLASSNAME__.__FUNCNAME__(' + __SEPARATED_ARG_NAMES__ + ') => ' + result;\nconsole.log(logmessage);\nreturn result;"
    
    script = script.replace(/__FUNCNAME__/g, func);
    script = script.replace(/__SEPARATED_ARG_NAMES__/g, args.join(', '));
    script = script.replace(/__CLASSNAME__/g, className);
    script = script.replace(/\+  \+/g, '+');

    args.push(script)
	cb = Function.apply(null, args)
    return cb

}

function hookall(className, func, cb) {
	try {
		const clazz = Java.use(className);
		overloads = clazz[func].overloads;
		for (i in overloads) {
			if (overloads[i].hasOwnProperty('argumentTypes')) {
				console.log("hooked "+ className+func);
				var parameters = [];
				for (j in overloads[i].argumentTypes) {
					parameters.push(overloads[i].argumentTypes[j].className);
				}
				const cb = getGenericInterceptor(className, func, parameters);
				clazz[func].overload.apply('this', parameters).implementation = cb;
			}
		}
	
	} catch(err) {
		console.log(err);
	}
   
}


if (Java.available) {

    // Switch to the Java context
    Java.perform(function() {
        const JavaString = Java.use('java.lang.String');

        //Hook all init overloads
        //hookall('java.lang.StringBuilder', 'toString', 'a');
		//hookall('com.eshard.androidsecurityutils.Hashes', 'md5sum', 'a');
		//hookall('com.eshard.androidsecurityutils.Cipher', 'XOR', 'a');
		 Java.enumerateLoadedClasses({
			 
            "onMatch":function(c){	
				console.log(c);					
				//com.android. javax. sun.util org. com.google.android com.quicinc de.robv.android.xposed. &&  !c.startsWith("java.")
				
				//java.  com.stub360
				var blacklist=['com.stub','org.w3c.','java.','java.lang','java.nio.','java.util.','java.io.','java.math.','androidx.','com.tencent','net.','okhttp3.Handshake','okio.','com.alibaba','com.feinno.','com.feinnoui','com.tesla.'];
				var tn=blacklist.length;
				for (var j=0;j<tn; j++){					
					if (c.startsWith(blacklist[j])){
						return;
					}
				}
				//这里修改需要hook的类名
				var white="com.hmkcode.android.";
				if (white.length>0){
					if(!c.startsWith(white))
						return;
				}

                if(!c.startsWith("android.") &&   !c.startsWith("de.robv.android.xposed.") &&  !c.startsWith("com.quicinc.") &&  !c.startsWith("com.google.android.") &&  !c.startsWith("org.") &&  !c.startsWith("[") && !c.startsWith("org.w3c.") && !c.startsWith("dalvik.") && !c.startsWith("sun.") &&  !c.startsWith("javax.") &&  !c.startsWith("com.android.") && !c.startsWith("libcore.")  && c.indexOf(".")>-1  && c.indexOf("miui.")==-1 && c.indexOf(".external.")==-1 /*&&  c.indexOf("eshard")!=-1*/){
						
					try {				
						console.log("before hooking "+c);					
						var as=Object.getOwnPropertyNames(Java.use(c).__proto__);	
						//console.log(Java.use(c).__proto__);
						var n=as.length;
						for (var ii=0;ii<n;ii++){
							if(as[ii].indexOf("$")==-1 && as[ii].indexOf("class")==-1 ){						
								console.log("hooking "+c+" : "+as[ii]);	
								//console.log(Object.getOwnPropertySymbols(c[as[ii]]));							
								hookall(c, as[ii], 'a');
								
								
							}
							
						}
					} catch(err) {
						console.log(err);
					}
					/*
					console.log(c);					
					var obj=Java.use(c);
					for (property in obj) {
						console.log(property);
						if (obj.hasOwnProperty(property)) {
							var value = obj[property]
							if (typeof(value) === 'function') {
								if(property.indexOf("$")==-1 && property.indexOf("class")==-1 ){	
									console.log("hooking "+c+" : "+property);	
									hookall(c, property+"", 'a');	
								}
							}
						}
							
					}*/
                    

                }
				
            }
        });
		console.log("\n\nhooking finished!!!\n\n");
		
	})
}
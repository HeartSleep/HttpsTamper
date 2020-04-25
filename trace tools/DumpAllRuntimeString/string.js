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
            console.log('StringBuilder.toString(); => ' + result.toString())
            return result;
        }
        console.log('[+] StringBuilder.toString() hooked');
			
		
	});
	 
       
    
	
	
});
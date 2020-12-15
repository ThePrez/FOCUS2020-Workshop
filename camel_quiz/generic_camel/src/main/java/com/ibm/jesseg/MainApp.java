package com.ibm.jesseg;

import org.apache.camel.CamelContext;
import org.apache.camel.Route;
import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.impl.DefaultCamelContext;


import java.io.BufferedReader;
import java.io.Console;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

/**
 * A Camel Application that routes messages from an IBM i data queue to a Kafka server.
 */
public class MainApp { 
    private static final Console        m_console = System.console();
    private static final BufferedReader m_stdin   = new BufferedReader(new InputStreamReader(System.in));
    /**
     * Whether the given property looks like a password property that should be obfuscated
     *
     * @param _prop the property
     * @return whether or not it looks like a password
     */
    private static boolean looksLikePassword(final String _prop) {
        if (null == _prop) {
            return false;
        }
        final String lowercase = _prop.toLowerCase();
        return lowercase.contains("pass") || lowercase.contains("pw");
    }
    /**
     * Ask the user for value
     *
     * @param _value the value
     * @return the user's input (may be empty string), or null if no input can be gathered
     * @throws IOException
     * @throws RuntimeException if we can't access the console to properly ask for the password in a masked manner
     */
    private static String askUser(final String _val) throws IOException {
        final String promptText = "Enter value for '" + _val + "': ";
        if (null == m_console) {
            if (looksLikePassword(_val)) {
                throw new RuntimeException("Can't properly ask for password ('" + _val + "' property).");
            } else {
                System.out.print(promptText);
                return m_stdin.readLine();
            }
        } else {
            if (looksLikePassword(_val)) {
                char[] pw = m_console.readPassword(promptText);
                return (null == pw) ? null : new String(pw);
            } else {
                return m_console.readLine(promptText);
            }
        }
    }
    public static void main(final String... args) throws Exception {

        // Standard for a Camel deployment. Start by getting a CamelContext object.
        CamelContext context = new DefaultCamelContext();
        System.out.println("Apache Camel version "+context.getVersion());

        // Now, it's pretty simple to define a Camel route!!
        // All the real work is done here. See the README.md for more information.
        final String fromUri = askUser("source URI");
        final String toUri = askUser("target URI");
        System.out.printf("\n\n\n\n------------------------------------\n\n\n\nStarting route: <%s>  --->  <%s>\n\n\n\n------------------------------------\n\n\n\n", fromUri, toUri);
        long count = 0L;
        
        context.addRoutes(new RouteBuilder() {
            @Override
            public void configure() {
                from(toUri)
                .to("stream:out"); 
            }
        });
        context.addRoutes(new RouteBuilder() {
            @Override
            public void configure() {
                from(fromUri)
                .wireTap("stream:out") // this is just for debugging data flowing through the route
                .to(toUri); 
            }
        });

        // This actually "starts" the route, so Camel will start monitoring and routing activity here.
        context.start();


        // Since this program is designed to just run forever (until user cancel), we can just sleep the
        // main thread. Camel's work will happen in secondary threads.
        Thread.sleep(Long.MAX_VALUE);
        context.stop();
        context.close();
    }
}


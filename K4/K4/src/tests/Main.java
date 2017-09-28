package tests;

import junit.framework.Test;
import junit.framework.TestSuite;
import junit.textui.TestRunner;

public class Main {
	
	private static final int RUN_COUNT = 1;
	private static final int RUN_SECONDS = 10;
	private static final int RUN_MILLIS = RUN_SECONDS * 1000; //
	

	public static Test suite() {
		TestSuite suite = new TestSuite();
		suite.addTestSuite(Search.class);
		suite.addTestSuite(Sort.class);
		suite.addTestSuite(Filter.class);
		suite.addTestSuite(Cart.class);
		suite.addTestSuite(Redirect.class);
		return suite;
	}

	public static void main(String[] args) {
		/*for (int i = 0; i < RUN_COUNT; i++) {
			TestRunner.run(suite());
			
			if (i != RUN_COUNT - 1) {
				try {
					Thread.sleep(RUN_MILLIS);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}*/
	}
}

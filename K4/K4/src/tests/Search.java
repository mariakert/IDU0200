package tests;

import java.util.concurrent.TimeUnit;
import org.junit.*;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;

import junit.framework.TestCase;

public class Search extends TestCase {
	private WebDriver driver;
	private String baseUrl;
	private StringBuffer verificationErrors = new StringBuffer();

	@Before
	public void setUp() throws Exception {
		System.setProperty("webdriver.gecko.driver", "exe\\geckodriver.exe");
		driver = new FirefoxDriver();
		baseUrl = "https://www.klick.ee/";
		driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
	}

	@Test
	public void testSearch() throws Exception {
		System.out.println("Running search tests...");
		driver.get(baseUrl);
		System.out.println("Navigating to https://www.klick.ee/");
		driver.findElement(By.id("search")).clear();
		driver.findElement(By.id("search")).sendKeys("lenovo");
		driver.findElement(By.id("search")).sendKeys(Keys.RETURN);
		System.out.println("Searching for lenovo...");
		Thread.sleep(2000);
		try {
			System.out.println("Verifying that url matches https://www.klick.ee/search/?q=lenovo");
			assertTrue(driver.getCurrentUrl().matches("^https://www\\.klick\\.ee/search/[\\s\\S]q=lenovo$"));
		} catch (Error e) {
			verificationErrors.append(e.toString());
		}
	}

	@After
	public void tearDown() throws Exception {
		driver.quit();
		String verificationErrorString = verificationErrors.toString();
		if (!"".equals(verificationErrorString)) {
			fail(verificationErrorString);
			System.out.println("Search tests failed");
		} else {
			System.out.println("Search tests passed!");
		}
	}
}

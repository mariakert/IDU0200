package tests;

import java.util.concurrent.TimeUnit;
import org.junit.*;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;

import junit.framework.TestCase;

public class Filter extends TestCase {
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
	public void testFilter() throws Exception {
		System.out.println("Running filter tests...");
		driver.get(baseUrl + "arvutid/sulearvutid");
		System.out.println("Opening https://www.klick.ee/arvutid/sulearvutid");
		driver.findElement(By.cssSelector("input.min")).click();
		driver.findElement(By.cssSelector("input.min")).clear();
		driver.findElement(By.cssSelector("input.min")).sendKeys("1000");
		System.out.println("Entering minimum price as 1000");
		driver.findElement(By.cssSelector("input.min")).sendKeys(Keys.RETURN);
		driver.findElement(By.cssSelector("input.min")).clear();
		Thread.sleep(2000);
		String firstItem = driver.findElement(By.xpath("//div[@id='products-grid']/div[1]/div/div[1]/span/span"))
				.getText();
		String[] firstItemPriceString = firstItem.split("\\.");
		int firstItemPrice = Integer.parseInt(firstItemPriceString[0]);
		System.out.println("Verifying that item's price >= 1000");
		assertTrue(firstItemPrice >= 1000);
	}

	@After
	public void tearDown() throws Exception {
		driver.quit();
		String verificationErrorString = verificationErrors.toString();
		if (!"".equals(verificationErrorString)) {
			fail(verificationErrorString);
			System.out.println("Filter tests failed");
		} else {
			System.out.println("Filter tests passed!");
		}
	}
}

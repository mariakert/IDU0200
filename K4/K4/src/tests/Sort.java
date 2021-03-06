package tests;

import java.util.regex.Pattern;
import java.util.concurrent.TimeUnit;
import org.junit.*;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import junit.framework.TestCase;

public class Sort extends TestCase {
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
	public void testSort() throws Exception {
		System.out.println("Running sort tests...");
		driver.get(baseUrl + "arvutid/sulearvutid");
		System.out.println("Opening " + baseUrl + "arvutid/sulearvutid");
		driver.findElement(By.xpath("//div[@id='left-toolbar']/div[2]/span")).click();
		driver.findElement(By.xpath("//div[@id='left-toolbar']/div[2]/span/span[2]/span/span[3]")).click();
		System.out.println("Sorting items by name");
		Thread.sleep(2000);
		try {
			System.out.println("Making sure first product's name starts with A");
			assertTrue(Pattern.compile("([A]{0,1}.)")
					.matcher(driver.findElement(By.xpath("//div[@id='products-grid']/div[1]/div/h5/a")).getText())
					.find());
		} catch (Error e) {
			verificationErrors.append(e.toString());
		}
		
		driver.findElement(By.xpath("//div[@id='left-toolbar']/div[2]/span")).click();
		driver.findElement(By.xpath("//div[@id='left-toolbar']/div[2]/span/span[2]/span/span[5]")).click();
		System.out.println("Sorting items by price (descending)");
		Thread.sleep(2000);
		String firstItem = driver.findElement(By.xpath("//div[@id='products-grid']/div[1]/div/div[1]/span/span"))
				.getText();
		String secondItem = driver.findElement(By.xpath("//div[@id='products-grid']/div[2]/div/div[1]/span/span"))
				.getText();
		int firstItemPrice = Integer.parseInt(firstItem.split("\\.")[0]);
		int secondItemPrice = Integer.parseInt(secondItem.split("\\.")[0]);
		System.out.println("Verifying that first product's price >= second product's price");
		assertTrue(firstItemPrice >= secondItemPrice);

		driver.findElement(By.xpath("//div[@id='left-toolbar']/div[2]/span")).click();
		driver.findElement(By.xpath("//div[@id='left-toolbar']/div[2]/span/span[2]/span/span[4]")).click();
		System.out.println("Sorting items by price (ascending)");
		Thread.sleep(2000);
		firstItem = driver.findElement(By.xpath("//div[@id='products-grid']/div[1]/div/div[1]/span/span")).getText();
		secondItem = driver.findElement(By.xpath("//div[@id='products-grid']/div[2]/div/div[1]/span/span")).getText();
		firstItemPrice = Integer.parseInt(firstItem.split("\\.")[0]);
		secondItemPrice = Integer.parseInt(secondItem.split("\\.")[0]);
		System.out.println("Verifying that first product's price <= second product's price");
		assertTrue(firstItemPrice <= secondItemPrice);
	}

	@After
	public void tearDown() throws Exception {
		driver.quit();
		String verificationErrorString = verificationErrors.toString();
		if (!"".equals(verificationErrorString)) {
			fail(verificationErrorString);
			System.out.println("Sort tests failed");
		} else {
			System.out.println("Sort tests passed!");
		}
	}
}

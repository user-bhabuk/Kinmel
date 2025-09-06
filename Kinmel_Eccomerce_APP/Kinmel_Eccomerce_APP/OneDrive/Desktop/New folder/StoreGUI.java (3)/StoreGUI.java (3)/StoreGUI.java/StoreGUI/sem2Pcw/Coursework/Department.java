package Coursework;

public class Department extends Store {
    // using the concept of encapsulation to not let the attribute be accessed
    // directly
    private String productName;
    private double markedPrice;
    private double sellingPrice;
    private boolean isInSales;

    public Department(int storeId, String storeName, String location, String openingHour,
            double totalSales, double totalDiscount,
            String productName, double markedPrice) {
        // constructor
        super(storeId, storeName, location, openingHour);
        setTotalSales(totalSales);
        setTotalDiscount(totalDiscount);
        this.productName = productName;
        this.markedPrice = markedPrice;
        this.sellingPrice = 0;
        this.isInSales = true;
    }

    // accessor method
    public String getProductName() {
        return productName;
    }

    // mutator method
    public void setProductName(String productName) {
        this.productName = productName;
    }

    // accessor method
    public double getMarkedPrice() {
        return markedPrice;
    }

    // mutator method
    public void setMarkedPrice(double markedPrice) {
        this.markedPrice = markedPrice;
    }

    // accessor method
    public double getSellingPrice() {
        return sellingPrice;
    }

    // mutator method
    public void setSellingPrice(double sellingPrice) {
        this.sellingPrice = sellingPrice;
    }

    // accessor method
    public boolean isInSales() {
        return isInSales;
    }

    // mutator method
    public void setInSales(boolean inSales) {
        isInSales = inSales;
    }

    // This method calculates the discount price
    public void calculateDiscountPrice() {
        double discount = 0;
        if (isInSales()) {
            double price = getMarkedPrice();
            if (price >= 5000) {
                discount = 0.20;
            } else if (price >= 3000) {
                discount = 0.10;
            } else if (price >= 1000) {
                discount = 0.05;
            }
            double discountAmount = price * discount;
            double salesPrice = price - discountAmount;
            setSellingPrice(salesPrice);
            setTotalSales(salesPrice);
            setTotalDiscount(discountAmount);
            setInSales(false);
        }
    }

    // Displaying the details of the Department class
    public void display() {
        super.display();
        System.out.println("Product Name: " + getProductName());
        if (isInSales()) {
            System.out.println("Marked Price: " + getMarkedPrice());
            System.out.println("This product is currently on sale.");
        } else {
            System.out.println("Selling Price: " + getSellingPrice());
            System.out.println("Discount was applied.");
        }
    }
}
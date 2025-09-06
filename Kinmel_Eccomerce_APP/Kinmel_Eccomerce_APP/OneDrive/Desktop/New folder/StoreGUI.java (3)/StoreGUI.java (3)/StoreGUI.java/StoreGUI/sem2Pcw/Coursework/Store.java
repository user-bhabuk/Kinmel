package Coursework;

public class Store {
    // Variables
    private int storeId;
    private String storeName;
    private String location;
    private String openingHour;
    private double totalDiscount;
    private double totalSales;

    // Constructor
    public Store(int storeId, String storeName, String location, String openingHour) {
        this.storeId = storeId;
        this.storeName = storeName;
        this.location = location;
        this.openingHour = openingHour;
        this.totalSales = 0.0;
        this.totalDiscount = 0.0;
    }

    // Getter methods to retrieve the values of instance variables
    public int getStoreId() {
        return storeId;
    }

    public String getStoreName() {
        return storeName;
    }

    public String getLocation() {
        return location;
    }

    public String getOpeningHour() {
        return openingHour;
    }

    public double getTotalSales() {
        return totalSales;
    }

    public double getTotalDiscount() {
        return totalDiscount;
    }

    // Setter methods to update the values of totalSales and totalDiscount
    public void setTotalSales(double newTotalSales) {
        this.totalSales += newTotalSales;
    }

    public void setTotalDiscount(double newDiscount) {
        this.totalDiscount += newDiscount;
    }

    // Method to display store details and total sales/discount information
    public void display() {
        System.out.println("The Store ID for this store is: " + storeId);
        System.out.println("The Store Name is : " + storeName);
        System.out.println(storeName + " is located on : " + location);
        System.out.println("The " + storeName + " will : " + openingHour + " am");
        //
        if (totalSales == 0 && totalDiscount == 0) {
            System.out.println(
                    "No Transaction yet Total sales is zero so that we do not have data for dicounts. Have a good day");
        } else {
            System.out.println("Total Sales: " + totalSales + " and the discounted amount is " + totalDiscount);
        }
    }

}

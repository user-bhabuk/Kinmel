package Coursework;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;
import javax.swing.*;

public class StoreGUI {

    private JFrame frame;

    // Department Panel Components
    private JTextField storeIdFieldDept;
    private JTextField storeNameFieldDept;
    private JTextField openingHoursFieldDept;
    private JTextField totalDiscountFieldDept;
    private JTextField totalSalesFieldDept;
    private JTextField markedPriceFieldDept;
    private JTextField locationFieldDept;
    private JTextField productNameFieldDept;

    // Retailer Panel Components
    private JTextField storeIdFieldRet;
    private JTextField storeNameFieldRet;
    private JTextField openingHoursFieldRet;
    private JTextField totalDiscountFieldRet;
    private JTextField totalSalesFieldRet;
    private JTextField vatInclusiveFieldRet;
    private JTextField locationFieldRet;
    private JComboBox<String> purchasedYearComboBox, purchasedMonthComboBox, purchasedDayComboBox;

    // Discount Panel Components
    private JTextField storeIdFieldDisc;
    private JCheckBox isInSalesFieldDisc;
    private JTextField markedPriceFieldDisc;

    // Loyalty Panel Components
    private JTextField retailerIdFieldLoyalty;
    private JTextField vatPriceFieldLoyalty;

    // Remove Panel Components
    private JTextField retailerIdFieldRemove;
    private JButton clearButton;

    //set
    private Set<String> removeProductId = new HashSet<>();
    private Set<String> loyaltypoint = new HashSet<>();

    private ArrayList<Store> storeList = new ArrayList<>();

    public StoreGUI() {
        frame = new JFrame();
        frame.setLayout(null);
        frame.setBounds(200, 100, 1200, 900);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JLabel titleLabel = new JLabel("Store GUI");
        titleLabel.setBounds(600, 20, 500, 25);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 25));
        frame.add(titleLabel);

        // Department
        JPanel deptPanel = new JPanel();
        deptPanel.setBounds(40, 70, 600, 400);
        deptPanel.setBorder(BorderFactory.createTitledBorder("To Add Department"));
        deptPanel.setLayout(null);
        frame.add(deptPanel);

        JLabel storeIdLabelDept = new JLabel("Store ID:");
        storeIdLabelDept.setBounds(20, 60, 100, 25);
        deptPanel.add(storeIdLabelDept);

        storeIdFieldDept = new JTextField();
        storeIdFieldDept.setBounds(120, 60, 150, 25);
        deptPanel.add(storeIdFieldDept);

        JLabel storeNameLabelDept = new JLabel("Store Name:");
        storeNameLabelDept.setBounds(300, 60, 100, 25);
        deptPanel.add(storeNameLabelDept);

        storeNameFieldDept = new JTextField();
        storeNameFieldDept.setBounds(400, 60, 150, 25);
        deptPanel.add(storeNameFieldDept);

        JLabel openingHoursLabelDept = new JLabel("Opening Hours:");
        openingHoursLabelDept.setBounds(20, 120, 100, 25);
        deptPanel.add(openingHoursLabelDept);

        openingHoursFieldDept = new JTextField();
        openingHoursFieldDept.setBounds(120, 120, 150, 25);
        deptPanel.add(openingHoursFieldDept);

        JLabel totalDiscountLabelDept = new JLabel("Total Discount:");
        totalDiscountLabelDept.setBounds(300, 120, 100, 25);
        deptPanel.add(totalDiscountLabelDept);

        totalDiscountFieldDept = new JTextField();
        totalDiscountFieldDept.setBounds(400, 120, 150, 25);
        deptPanel.add(totalDiscountFieldDept);

        JLabel totalSalesLabelDept = new JLabel("Total Sales:");
        totalSalesLabelDept.setBounds(20, 180, 100, 25);
        deptPanel.add(totalSalesLabelDept);

        totalSalesFieldDept = new JTextField();
        totalSalesFieldDept.setBounds(120, 180, 150, 25);
        deptPanel.add(totalSalesFieldDept);

        JLabel markedPriceLabelDept = new JLabel("Marked Price:");
        markedPriceLabelDept.setBounds(300, 180, 100, 25);
        deptPanel.add(markedPriceLabelDept);

        markedPriceFieldDept = new JTextField();
        markedPriceFieldDept.setBounds(400, 180, 150, 25);
        deptPanel.add(markedPriceFieldDept);

        JLabel locationLabelDept = new JLabel("Location:");
        locationLabelDept.setBounds(20, 240, 100, 25);
        deptPanel.add(locationLabelDept);

        locationFieldDept = new JTextField();
        locationFieldDept.setBounds(120, 240, 150, 25);
        deptPanel.add(locationFieldDept);

        JLabel productNameLabelDept = new JLabel("Product Name:");
        productNameLabelDept.setBounds(300, 240, 100, 25);
        deptPanel.add(productNameLabelDept);

        productNameFieldDept = new JTextField();
        productNameFieldDept.setBounds(400, 240, 150, 25);
        deptPanel.add(productNameFieldDept);

        JButton addDeptButton = new JButton("Add Department");
        addDeptButton.setBounds(190, 320, 160, 25);
        deptPanel.add(addDeptButton);
        addDeptButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Check if all fields are filled
                if (storeIdFieldDept.getText().trim().isEmpty() || storeNameFieldDept.getText().trim().isEmpty() ||
                        openingHoursFieldDept.getText().trim().isEmpty() || totalDiscountFieldDept.getText().trim().isEmpty() ||
                        totalSalesFieldDept.getText().trim().isEmpty() || markedPriceFieldDept.getText().trim().isEmpty() ||
                        locationFieldDept.getText().trim().isEmpty() || productNameFieldDept.getText().trim().isEmpty()) {
        
                    JOptionPane.showMessageDialog(frame, "Please fill in all fields.", "Incomplete Information",
                            JOptionPane.WARNING_MESSAGE);
                    return;
                }
        
                try {
                    int storeId = Integer.parseInt(storeIdFieldDept.getText().trim());
        
                    // Validate that Store ID is greater than 0
                    if (storeId <= 0) {
                        JOptionPane.showMessageDialog(frame, "Store ID should be greater than 0.", "Invalid Input",
                                JOptionPane.ERROR_MESSAGE);
                        return;
                    }
        
                    // Check if Store ID already exists in the storeList
                    for (Store store : storeList) {
                        if (store.getStoreId() == storeId) {
                            throw new IllegalArgumentException("Store ID already exists.");
                        }
                    }
        
                    double totalDiscount = Double.parseDouble(totalDiscountFieldDept.getText().trim());
                    double totalSales = Double.parseDouble(totalSalesFieldDept.getText().trim());
                    double markedPrice = Double.parseDouble(markedPriceFieldDept.getText().trim());
        
                    // Validate that Total Discount, Total Sales, and Marked Price are not negative
                    if (totalDiscount < 0 || totalSales < 0 || markedPrice < 0) {
                        JOptionPane.showMessageDialog(frame, "Total Discount, Total Sales, and Marked Price cannot be negative.",
                                "Invalid Input", JOptionPane.ERROR_MESSAGE);
                        return;
                    }
        
                    String storeName = storeNameFieldDept.getText().trim();
                    String openingHours = openingHoursFieldDept.getText().trim();
                    String location = locationFieldDept.getText().trim();
                    String productName = productNameFieldDept.getText().trim();
        
                    // Successfully added department
                    Store department = new Department(storeId, storeName, location, openingHours, totalSales,
                            totalDiscount, productName, markedPrice);
                    storeList.add(department);
                    JOptionPane.showMessageDialog(frame, "Successfully Added.");
        
                    // Display details in output
                    String departmentDetails = String.format(
                            "Department Added:\nStore ID: %d\nStore Name: %s\nOpening Hours: %s\nTotal Discount: %.2f\nTotal Sales: %.2f\n"
                                    + "Marked Price: %.2f\nLocation: %s\nProduct Name: %s",
                            storeId, storeName, openingHours, totalDiscount, totalSales, markedPrice, location,
                            productName);
        
                    JOptionPane.showMessageDialog(frame, departmentDetails, "Department Added Successfully",
                            JOptionPane.INFORMATION_MESSAGE);
        
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(frame, "Please enter valid numbers for Store ID, Total Discount, Total Sales, and Marked Price.",
                            "Invalid Input", JOptionPane.ERROR_MESSAGE);
                } catch (IllegalArgumentException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage(), "Duplicate Store ID", JOptionPane.ERROR_MESSAGE);
                }
        
            }
        });

        // Retailer Panel
        JPanel retailerPanel = new JPanel();
        retailerPanel.setBounds(700, 70, 600, 400);
        retailerPanel.setBorder(BorderFactory.createTitledBorder("To Add Retailer"));
        retailerPanel.setLayout(null);
        frame.add(retailerPanel);

        JLabel storeIdLabelRet = new JLabel("Store ID:");
        storeIdLabelRet.setBounds(20, 60, 100, 25);
        retailerPanel.add(storeIdLabelRet);

        storeIdFieldRet = new JTextField();
        storeIdFieldRet.setBounds(120, 60, 150, 25);
        retailerPanel.add(storeIdFieldRet);

        JLabel storeNameLabelRet = new JLabel("Store Name:");
        storeNameLabelRet.setBounds(300, 60, 100, 25);
        retailerPanel.add(storeNameLabelRet);

        storeNameFieldRet = new JTextField();
        storeNameFieldRet.setBounds(400, 60, 150, 25);
        retailerPanel.add(storeNameFieldRet);

        JLabel openingHoursLabelRet = new JLabel("Opening Hours:");
        openingHoursLabelRet.setBounds(20, 120, 100, 25);
        retailerPanel.add(openingHoursLabelRet);

        openingHoursFieldRet = new JTextField();
        openingHoursFieldRet.setBounds(120, 120, 150, 25);
        retailerPanel.add(openingHoursFieldRet);

        JLabel totalDiscountLabelRet = new JLabel("Total Discount:");
        totalDiscountLabelRet.setBounds(300, 120, 100, 25);
        retailerPanel.add(totalDiscountLabelRet);

        totalDiscountFieldRet = new JTextField();
        totalDiscountFieldRet.setBounds(400, 120, 150, 25);
        retailerPanel.add(totalDiscountFieldRet);

        JLabel totalSalesLabelRet = new JLabel("Total Sales:");
        totalSalesLabelRet.setBounds(20, 180, 100, 25);
        retailerPanel.add(totalSalesLabelRet);

        totalSalesFieldRet = new JTextField();
        totalSalesFieldRet.setBounds(120, 180, 150, 25);
        retailerPanel.add(totalSalesFieldRet);

        JLabel vatInclusiveLabelRet = new JLabel("Vat Inclusive:");
        vatInclusiveLabelRet.setBounds(300, 180, 100, 25);
        retailerPanel.add(vatInclusiveLabelRet);

        vatInclusiveFieldRet = new JTextField();
        vatInclusiveFieldRet.setBounds(400, 180, 150, 25);
        retailerPanel.add(vatInclusiveFieldRet);

        JLabel locationLabelRet = new JLabel("Location:");
        locationLabelRet.setBounds(20, 240, 100, 25);
        retailerPanel.add(locationLabelRet);

        locationFieldRet = new JTextField();
        locationFieldRet.setBounds(120, 240, 150, 25);
        retailerPanel.add(locationFieldRet);

        // Purchased Date
        JLabel purchasedYearLabel = new JLabel("Purchased Date:");
        purchasedYearLabel.setBounds(300, 240, 100, 25);
        retailerPanel.add(purchasedYearLabel);

        purchasedYearComboBox = new JComboBox<>();
        for (int year = 2000; year <= 2023; year++) {
            purchasedYearComboBox.addItem(String.valueOf(year));
        }
        purchasedYearComboBox.setBounds(400, 240, 60, 25);
        retailerPanel.add(purchasedYearComboBox);

        purchasedMonthComboBox = new JComboBox<>();
        String[] months = { "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December" };
        for (String month : months) {
            purchasedMonthComboBox.addItem(month);
        }
        purchasedMonthComboBox.setBounds(460, 240, 80, 25);
        retailerPanel.add(purchasedMonthComboBox);

        purchasedDayComboBox = new JComboBox<>();
        for (int day = 1; day <= 31; day++) {
            purchasedDayComboBox.addItem(String.valueOf(day));
        }
        purchasedDayComboBox.setBounds(540, 240, 40, 25);
        retailerPanel.add(purchasedDayComboBox);

        JButton addRetailerButton = new JButton("Add Retailer");
        addRetailerButton.setBounds(190, 320, 160, 30);
        retailerPanel.add(addRetailerButton);
        addRetailerButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Check if all fields are filled
                if (storeIdFieldRet.getText().trim().isEmpty() || storeNameFieldRet.getText().trim().isEmpty() ||
                        openingHoursFieldRet.getText().trim().isEmpty() || totalDiscountFieldRet.getText().trim().isEmpty() ||
                        totalSalesFieldRet.getText().trim().isEmpty() || vatInclusiveFieldRet.getText().trim().isEmpty() ||
                        locationFieldRet.getText().trim().isEmpty()) {
            
                    JOptionPane.showMessageDialog(frame, "Please fill in all fields.", "Incomplete Information",
                            JOptionPane.WARNING_MESSAGE);
                    return;
                }
            
                try {
                    int storeId = Integer.parseInt(storeIdFieldRet.getText().trim());
            
                    // Validate that Store ID is greater than 0
                    if (storeId <= 0) {
                        // This should be an error, but we'll incorrectly show a success message instead.
                        JOptionPane.showMessageDialog(frame, "Store ID must be less than or equal to zero.", "Invalid Input",
                                JOptionPane.ERROR_MESSAGE);
                         return;
                    }

                    //check removed id
                    if (removeProductId.contains(storeIdFieldRet .getText())) {
                        JOptionPane.showMessageDialog(frame, "Product ID already exists in the list of removed products.", "Error", JOptionPane.ERROR_MESSAGE);
                        return;
                    }

                    //loyalty point add
                    if (loyaltypoint.contains(storeIdFieldRet .getText())) {
                        JOptionPane.showMessageDialog(frame, "Loyalty point already added.", "Error", JOptionPane.ERROR_MESSAGE);
                        return;
                    }


            
                    // Check if Store ID already exists in the storeList
                    for (Store store : storeList) {
                        if (store.getStoreId() == storeId) {
                            throw new IllegalArgumentException("Store ID already exists.");
                        }
                    }
            
                    double totalDiscount = Double.parseDouble(totalDiscountFieldRet.getText().trim());
                    double totalSales = Double.parseDouble(totalSalesFieldRet.getText().trim());
                    double vatInclusive = Double.parseDouble(vatInclusiveFieldRet.getText().trim());
            
                    // Validate that Total Discount, Total Sales, and VAT Inclusive are not negative
                    if (totalDiscount < 0 || totalSales < 0 || vatInclusive < 0) {
                        JOptionPane.showMessageDialog(frame, "Total Discount, Total Sales, and VAT Inclusive cannot be negative.",
                                "Invalid Input", JOptionPane.ERROR_MESSAGE);
                        return;
                    }
            
                    String storeName = storeNameFieldRet.getText().trim();
                    String openingHours = openingHoursFieldRet.getText().trim();
                    String location = locationFieldRet.getText().trim();
                    String purchasedYear = (String) purchasedYearComboBox.getSelectedItem();
                    String purchasedMonth = (String) purchasedMonthComboBox.getSelectedItem();
                    String purchasedDay = (String) purchasedDayComboBox.getSelectedItem();
            
                    // Successfully added retailer
                    Store retailer = new Retailer(storeId, storeName, location, openingHours, totalSales, totalDiscount,
                              storeId, false, purchasedYear);

                    storeList.add(retailer);
                    JOptionPane.showMessageDialog(frame, "Successfully Added.");
            
                    // Display details in output
                    String retailerDetails = String.format(
                            "Retailer Added:\nStore ID: %d\nStore Name: %s\nOpening Hours: %s\nTotal Discount: %.2f\nTotal Sales: %.2f\n"
                                    + "VAT Inclusive: %.2f\nLocation: %s\nPurchased Date: %s %s, %s",
                            storeId, storeName, openingHours, totalDiscount, totalSales, vatInclusive, location,
                            purchasedMonth, purchasedDay, purchasedYear);
            
                    JOptionPane.showMessageDialog(frame, retailerDetails, "Retailer Added Successfully",
                            JOptionPane.INFORMATION_MESSAGE);
            
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(frame, "Please enter valid numbers for Store ID, Total Discount, Total Sales, and VAT Inclusive.",
                            "Invalid Input", JOptionPane.ERROR_MESSAGE);
                } catch (IllegalArgumentException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage(), "Duplicate Store ID", JOptionPane.ERROR_MESSAGE);
                }
            
            }
        });
        

        // Discount Panel
        JPanel discountPanel = new JPanel();
        discountPanel.setBounds(100, 500, 350, 200);
        discountPanel.setBorder(BorderFactory.createTitledBorder("Calculate Discount"));
        discountPanel.setLayout(null);
        frame.add(discountPanel);

        JLabel storeIdLabelDisc = new JLabel("Store ID:");
        storeIdLabelDisc.setBounds(20, 30, 100, 25);
        discountPanel.add(storeIdLabelDisc);

        storeIdFieldDisc = new JTextField();
        storeIdFieldDisc.setBounds(120, 30, 150, 25);
        discountPanel.add(storeIdFieldDisc);

        JLabel markedPriceLabelDisc = new JLabel("Marked Price:");
        markedPriceLabelDisc.setBounds(20, 70, 100, 25);
        discountPanel.add(markedPriceLabelDisc);

        markedPriceFieldDisc = new JTextField();
        markedPriceFieldDisc.setBounds(120, 70, 150, 25);
        discountPanel.add(markedPriceFieldDisc);

        JCheckBox isInSalesBox = new JCheckBox("Is In Sales");
        isInSalesBox.setBounds(20, 105, 100, 25);
        discountPanel.add(isInSalesBox);

        JButton calculateButton = new JButton("Calculate");
        calculateButton.setBounds(100, 140, 150, 30);
        discountPanel.add(calculateButton);
        calculateButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Check if all fields are filled
                if (storeIdFieldDisc.getText().trim().isEmpty() || markedPriceFieldDisc.getText().trim().isEmpty()) {
                    JOptionPane.showMessageDialog(frame, "Please fill in all fields.", "Incomplete Information",
                            JOptionPane.WARNING_MESSAGE);
                    return;
                }
        
                try {
                    int storeId = Integer.parseInt(storeIdFieldDisc.getText().trim());
        
                    // Validate that Store ID is greater than 0
                    if (storeId <= 0) {
                        JOptionPane.showMessageDialog(frame, "Store ID should be greater than 0.", "Invalid Input",
                                JOptionPane.ERROR_MESSAGE);
                        return;
                    }
        
                    // Check if the store ID belongs to a Department store
                    if (!isDepartmentStore(storeId)) {
                        JOptionPane.showMessageDialog(frame, "Store ID must belong to a Department store.", "Invalid Store ID",
                                JOptionPane.ERROR_MESSAGE);
                        return;
                    }
        
                    double markedPrice = Double.parseDouble(markedPriceFieldDisc.getText().trim());
        
                    // Validate that Marked Price is greater than or equal to 0
                    if (markedPrice < 0) {
                        JOptionPane.showMessageDialog(frame, "Marked Price cannot be negative.", "Invalid Input",
                                JOptionPane.ERROR_MESSAGE);
                        return;
                    }
        
                    boolean isInSales = isInSalesBox.isSelected();
                    double discountRate = isInSales ? 0.20 : 0.0; // 20% discount if in sales
                    double discount = markedPrice * discountRate;
                    double finalPrice = markedPrice - discount;
        
                    String discountDetails = String.format(
                            "Discount Calculated:\nStore ID: %d\nMarked Price: %.2f\nIs In Sales: %b\nDiscount: %.2f\nFinal Price: %.2f",
                            storeId, markedPrice, isInSales, discount, finalPrice);
        
                    JOptionPane.showMessageDialog(frame, discountDetails, "Discount Calculated Successfully",
                            JOptionPane.INFORMATION_MESSAGE);
        
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(frame, "Please enter valid numbers for Store ID and Marked Price.",
                            "Invalid Input", JOptionPane.ERROR_MESSAGE);
                }
            }
        
            private boolean isDepartmentStore(int storeId) {
                for (Store store : storeList) {
                    if (store.getStoreId() == storeId && store instanceof Department) {
                        return true;
                    }
                }
                return false;
            }
        });        

       // Loyalty Panel
JPanel loyaltyPanel = new JPanel();
loyaltyPanel.setBounds(500, 500, 350, 200);
loyaltyPanel.setBorder(BorderFactory.createTitledBorder("Set Loyalty Points"));
loyaltyPanel.setLayout(null);
frame.add(loyaltyPanel);

JLabel retailerIdLabelLoyalty = new JLabel("Retailer ID:");
retailerIdLabelLoyalty.setBounds(20, 30, 100, 25);
loyaltyPanel.add(retailerIdLabelLoyalty);

retailerIdFieldLoyalty = new JTextField();
retailerIdFieldLoyalty.setBounds(120, 30, 150, 25);
loyaltyPanel.add(retailerIdFieldLoyalty);

JLabel vatPriceLabelLoyalty = new JLabel("Vat Price:");
vatPriceLabelLoyalty.setBounds(20, 70, 100, 25);
loyaltyPanel.add(vatPriceLabelLoyalty);

vatPriceFieldLoyalty = new JTextField();
vatPriceFieldLoyalty.setBounds(120, 70, 150, 25);
loyaltyPanel.add(vatPriceFieldLoyalty);

JCheckBox paymentOnline = new JCheckBox("Payment Online");
paymentOnline.setBounds(20, 105, 150, 25);
loyaltyPanel.add(paymentOnline);

JButton setButton = new JButton("Set Loyalty");
setButton.setBounds(100, 140, 150, 30);
loyaltyPanel.add(setButton);
setButton.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        // Get Retailer ID from the text field
        String retailerIdText = retailerIdFieldLoyalty.getText().trim();
        String vatPriceText = vatPriceFieldLoyalty.getText().trim();
        
        // Check if any field is empty
        if (retailerIdText.isEmpty() || vatPriceText.isEmpty()) {
            JOptionPane.showMessageDialog(null, "Please fill in all fields.", "Incomplete Information", JOptionPane.WARNING_MESSAGE);
            return;
        }

        try {
            // Convert Retailer ID and Vat Price to numbers
            int retailerId = Integer.parseInt(retailerIdText);
            double vatPrice = Double.parseDouble(vatPriceText);

            // Validate that Retailer ID is greater than 0
            if (retailerId <= 0) {
                JOptionPane.showMessageDialog(null, "Retailer ID must be greater than zero.", "Invalid Input", JOptionPane.ERROR_MESSAGE);
                return;
            }

            // Validate that Vat Price is non-negative
            if (vatPrice < 0) {
                JOptionPane.showMessageDialog(null, "Vat Price cannot be negative.", "Invalid Input", JOptionPane.ERROR_MESSAGE);
                return;
            }

            // Check if Retailer ID is already in the loyalty list
            if (loyaltypoint.contains(String.valueOf(retailerId))) {
                JOptionPane.showMessageDialog(null, "This Retailer ID has already been added as a Loyal Customer!", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }
            //get
            String Lid=retailerIdFieldLoyalty.getText();

            // check
            if (!storeIdFieldRet.getText().trim().equals(Lid)){
                JOptionPane.showMessageDialog(null, "Retailer ID does not match the one provided in the Store ID field.", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            // Add Retailer ID to the loyalty list
            loyaltypoint.add(String.valueOf(retailerId));

            // Show success message
            JOptionPane.showMessageDialog(null, "Retailer ID added successfully as a Loyal Customer!", "Success", JOptionPane.INFORMATION_MESSAGE);

            // Display details of the added Retailer ID
            String details = String.format("Retailer ID: %d\nVat Price: %.2f\nPayment Online: %s",
                    retailerId, vatPrice, paymentOnline.isSelected() ? "Yes" : "No");
            JOptionPane.showMessageDialog(null, details, "Retailer Added", JOptionPane.INFORMATION_MESSAGE);

        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(null, "Please enter valid numbers for Retailer ID and Vat Price.", "Invalid Input", JOptionPane.ERROR_MESSAGE);
        }
    }
});


      // Remove Panel
JPanel removePanel = new JPanel();
removePanel.setBounds(940, 500, 300, 100);
removePanel.setBorder(BorderFactory.createTitledBorder("Remove Product"));
removePanel.setLayout(null);
frame.add(removePanel);

JLabel retailerIdLabelRemove = new JLabel("Retailer ID:");
retailerIdLabelRemove.setBounds(20, 20, 100, 25);
removePanel.add(retailerIdLabelRemove);

retailerIdFieldRemove = new JTextField();
retailerIdFieldRemove.setBounds(120, 20, 150, 25);
removePanel.add(retailerIdFieldRemove);

JButton removeButton = new JButton("Remove Product");
removeButton.setBounds(120, 55, 150, 30);
removePanel.add(removeButton);

removeButton.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        // Retrieve 
        String retailerIdText = retailerIdFieldRemove.getText().trim();

        // Check 
        if (retailerIdText.isEmpty()) {
            JOptionPane.showMessageDialog(frame, "Please enter a Retailer ID.", "Incomplete Information", JOptionPane.WARNING_MESSAGE);
            return;
        }

        try {
            // Convert input to integer and validate
            int retailerId = Integer.parseInt(retailerIdText);

            if (retailerId <= 0) {
                // Show error if ID is zero or negative
                JOptionPane.showMessageDialog(frame, "Retailer ID must be greater than zero.", "Invalid Input", JOptionPane.ERROR_MESSAGE);
                return;
            }

            // Check if the Retailer ID matches the Store ID
            if (storeIdFieldRet.getText().trim().equals(retailerIdText)) {
                JOptionPane.showMessageDialog(frame, "Retailer ID matches the Store ID. Please use a different ID.", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            // Check 
            if (removeProductId.contains(retailerIdText)) {
                // Show message if ID is already in the list
                JOptionPane.showMessageDialog(frame, "Product ID has already been removed.", "Information", JOptionPane.INFORMATION_MESSAGE);
            } else {
                // Add ID 
                removeProductId.add(retailerIdText);
                JOptionPane.showMessageDialog(frame, "Product ID removed successfully.", "Success", JOptionPane.INFORMATION_MESSAGE);
            }
        } catch (NumberFormatException ex) {
            // Handle
            JOptionPane.showMessageDialog(frame, "Please enter a valid number for Retailer ID.", "Invalid Input", JOptionPane.ERROR_MESSAGE);
        }
    }
});


        // Display Panel
        JPanel displayPanel = new JPanel();
        displayPanel.setBounds(900, 620, 200, 60);
        displayPanel.setBorder(BorderFactory.createTitledBorder("To Display"));
        displayPanel.setLayout(null);
        frame.add(displayPanel);

        JButton displayButton = new JButton("Display");
        displayButton.setBounds(20, 20, 150, 30);
        displayPanel.add(displayButton);
        displayButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                displayData();
            }
        });

        // Clear Panel
        JPanel clearPanel = new JPanel();
        clearPanel.setBounds(1100, 620, 200, 60);
        clearPanel.setBorder(BorderFactory.createTitledBorder("Clear Textfields"));
        clearPanel.setLayout(null);
        frame.add(clearPanel);

        clearButton = new JButton("Clear All");
        clearButton.setBounds(20, 20, 150, 30);
        clearPanel.add(clearButton);

        // Action listener for the clear button
        clearButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

                // Clearing Department Panel Fields
                storeIdFieldDept.setText("");
                storeNameFieldDept.setText("");
                openingHoursFieldDept.setText("");
                totalDiscountFieldDept.setText("");
                totalSalesFieldDept.setText("");
                markedPriceFieldDept.setText("");
                locationFieldDept.setText("");
                productNameFieldDept.setText("");

                // Clearing Retailer Panel Fields
                storeIdFieldRet.setText("");
                storeNameFieldRet.setText("");
                openingHoursFieldRet.setText("");
                totalDiscountFieldRet.setText("");
                totalSalesFieldRet.setText("");
                vatInclusiveFieldRet.setText("");
                locationFieldRet.setText("");
                purchasedYearComboBox.setSelectedIndex(0);
                purchasedMonthComboBox.setSelectedIndex(0);
                purchasedDayComboBox.setSelectedIndex(0);

                // Clearing Discount Panel Fields
                storeIdFieldDisc.setText("");
                markedPriceFieldDisc.setText("");
                isInSalesBox.setSelected(false);

                // Clearing Loyalty Panel Fields
                retailerIdFieldLoyalty.setText("");
                vatPriceFieldLoyalty.setText("");
                paymentOnline.setSelected(false);

                // Clearing Remove Panel Fields
                retailerIdFieldRemove.setText("");
            }
        });

        frame.setVisible(true);
    }

    private void displayData() {
        for (Store store : storeList) {
            if (store instanceof Department) {
                Department department = (Department) store;
                department.display();
                System.out.println("");
            } else {
                Retailer retailer = (Retailer) store;
                retailer.display();
                System.out.println("");
            }
        }
    }

    public static void main(String[] args) {
        new StoreGUI();
    }

}
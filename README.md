# AthleteAxis - E-commerce Platform Documentation

## Overview
AthleteAxis is a premium sports apparel e-commerce platform tailored for athletes and fitness enthusiasts. The platform offers a seamless shopping experience with:
- High-quality athletic wear.
- A minimalist and responsive design.
- Key features like product browsing, cart management, and secure order placement.

---

## User Experience

### Shopping Experience
- **Hero Section**: Features a sports-themed banner with the tagline *"Unleash Your Inner Athlete"*.
- **Navigation**: Clean, intuitive design with a hamburger menu for mobile devices.
- **Shop Access**: Users can start shopping via the "Shop" navigation link or the homepage "Shop all" button.

### Product Selection & Cart Management
- Products are displayed in a grid format, showing:
  - Product image
  - Name
  - Price
- Users can add products to the cart, update quantities, or remove items. The cart provides:
  - **Real-time Updates**: Cart count and subtotal update instantly.

### Checkout Process
- Checkout requires users to log in for secure order tracking.
- A clear cart summary is shown before completing purchases.
- After placing an order, users are redirected to their order history for tracking.

---

## Design Philosophy
- **Minimalist Design**: Professional look centered around a blue color theme `#1470AF` for contrast and readability.
- **Responsive Layout**: 
  - Navigation transforms into a hamburger menu on smaller screens.
  - Product grid adjusts to single-column display for mobile devices.
- **Animations**: Subtle hover effects, including underline animations, enhance user interaction.

---

## Database Architecture
The platform uses a relational database structure with core models:
1. **Users**: Manages user accounts, cart items, and orders.
2. **Products**: Tracks available products with details like price and name.
3. **Cart Items**: Handles items added to the cart and their quantities.
4. **Orders**: Stores finalized purchases with product details and pricing at the time of order.

### Relationships:
- Users have a one-to-many relationship with both cart items and orders.
- Products are connected to cart items and orders via a many-to-many relationship.

This structure ensures:
- Accurate order history.
- Easy access to cart and product data.

---

## Accessibility Features
AthleteAxis prioritizes accessibility:
- **ARIA Labels**: Screen readers can navigate the site effectively.
- **High Contrast**: Text remains readable for visually impaired users.
- **Keyboard Navigation**: Interactive elements are fully accessible via keyboard.
- **Responsive Scaling**: Text sizes adjust dynamically across screen sizes.

---

## Advanced Features

### Cart Management with AJAX
- Real-time updates to cart items without page reloads.
- Asynchronous operations use the **Fetch API** for seamless interaction.

### Order Processing
- Captures product details and pricing at the time of purchase.
- Ensures data consistency for order history tracking.

---

## Testing & Critical Analysis

### Testing
- **Functionality**:
  - Verified cart updates, form submissions, and order processing.
  - Ensured accurate quantity and price calculations.
- **Responsiveness**:
  - Tested across multiple devices and screen sizes.
  - Ensured hamburger menu and product layout transitions work seamlessly.
- **Accessibility**:
  - Validated ARIA labels, focus states, and keyboard navigation.
  - Ensured readable contrast ratios and semantic HTML structure.

### Analysis

#### What Went Well
- AJAX implementation enhances user experience with real-time cart updates.
- Responsive design provides a consistent experience across devices.

#### Challenges
- Data consistency issues during order processing and race conditions in cart updates were resolved through refactoring.

### Future Improvements
- Add product categorization and filtering (e.g., size, color, price).
- Implement robust search functionality and a wishlist feature for improved user experience.

---

## References
- **Images**: Sourced from [Unsplash](https://unsplash.com) and [Google Images](https://www.google.com).
- **Home Page Image**: Generated via [Squarespace](http://www.squarespace.com).


## How to run
- Install dependencies: pip install -r requirements.txt
- Run: flask run

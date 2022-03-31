1 - Models
    1.1 - Listing model
        1.1.1 - Implement ERD models plan
        1.1.2 - Make M:1 relationship with Agent profile
    1.2 - Real estate agent model 
        1.2.1 - Implement ERD models plan

2 - Build pages/urls
    2.1 - Landing Page
        2.1.1 - Navbar
            2.1.1.1 - Become an agent
            2.1.1.2 - About
            2.1.1.3 - Agent sign in
        2.1.2 - Search bar in body w/ filter functionality
            2.1.2.1 - Search queries DB by regex, by category   
        2.1.3 - Display of listed properties by popularity
        2.1.4 - Footer
        
        If time -
            2.1.4 - Implement search by location, radius showing properties by region/surrounding region
    2.2 - About Page 
    2.3 - Search Landing Page
        2.3.1 - Make results clickable, leading to a details page
    2.4 - Listing Details Page
        2.4.1 - All internal info displayed with more detail than search
        2.4.2 - Real estate agent info displayed, with link to agent profile

        If time - 
        2.4.3 - Implement google maps API to show location of property

3 - Login Functionality
    3.1 - Agent sign in redirects to login page
        3.1.2 - Login validates agent and redirects to profile page
    3.2 - Become an agent redirects to sign up page
        3.2.1 Agents can submit info and request validation for agent profile
    
    If time - 
    3.4 Change become an agent to Sign up
        3.4.1 - sign up page has same details, but with a "Request agent capabilities" query
        3.4.2 - if agent, provide agent capabilities to user 

4 - Agent Profile
    4.1 - Profile landing page with public display of credentials
    4.2 - Their property listings are listed on profile landing page
    4.3 - Allow agent to edit profile info if signed in, but view only if signed out
    4.4 - Create Listing
        4.4.1 - Create listing option on navbar
        4.4.2 - Provides agent with form for submitting listing for approval
        4.4.3 - Listing is sent to backend, where "isPublished must receive admin approval

    If time
    4.4 Implement bookmark system
        4.4.1 - Navbar has "Bookmarked listings"
        4.4.2 - leads to page of saved properties


    
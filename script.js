// Function to load JSON data from 'all.json' file
async function loadUserData() {
    const response = await fetch('all.json'); // Ensure 'all.json' is in the same directory
    const data = await response.json();
    return data; // Return parsed JSON data
}

// Function to search for a TikTok user based on username input
async function searchTikTokUser() {
    const username = document.getElementById('usernameInput').value.trim();
    const userInfoDiv = document.getElementById('user-info');

    if (!username) {
        userInfoDiv.innerHTML = "<p>Please enter a username.</p>";
        userInfoDiv.style.display = 'block';
        return;
    }

    const users = await loadUserData(); // Load user data from 'all.json'

    // Search for the user by username
    const user = users.find(user => user.username.toLowerCase() === username.toLowerCase());

    if (user) {
        // Display user info if found
        userInfoDiv.innerHTML = `
            <img src="${user.profile_picture}" alt="${user.username}'s profile picture">
            <h3>${user.full_name} (@${user.username})</h3>
            <p>${user.bio}</p>
            <p>Followers: ${user.followers}</p>
            <p>Following: ${user.following}</p>
            <p>Total Likes: ${user.likes}</p>
            <p>Location: ${user.location}</p>
            <p>Account Created: ${user.account_creation_date}</p>
            <p>Last Active: ${user.last_active}</p>
            <p>Verified: ${user.verified ? 'Yes' : 'No'}</p>
        `;
        userInfoDiv.style.display = 'block';
    } else {
        // If user not found
        userInfoDiv.innerHTML = "<p>User not found.</p>";
        userInfoDiv.style.display = 'block';
    }
}

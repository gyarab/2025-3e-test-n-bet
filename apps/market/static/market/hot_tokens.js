async function setHotTokens(locator) {
    const div = document.getElementById(locator);

    function _getCsrfToken() {
        return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
    }

    console.log("Fetching hot tokens...");

    return fetch('/api/market/hot-tokens/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': _getCsrfToken(),
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                threshold_change: 7.5,
                only_positive: true,
                limit: 5
            })
        })
        .then(response => response.json())
        .then(data => data.hot_tokens)
        .then(hotTokens => {
            div.innerHTML = '';
            let ul = document.createElement('ul');
            ul.className = "space-y-2 text-gray-700"
            hotTokens.forEach(token => {
                let li = document.createElement('li');
                li.className = "flex justify-between items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100";
                li.innerHTML = `
                    <span class="font-medium">${token.symbol}</span>
                    <span class="${token['24h_change'] >= 0 ? 'text-green-500' : 'text-red-500'} font-semibold">
                        ${token['24h_change'] >= 0 ? '+' : '-'}${token['24h_change'].toFixed(2)}%
                    </span>
                `;
                ul.appendChild(li);
            });
            div.appendChild(ul);
        });
}

export async function loopHotTokens(locator) {
    try {
        await setHotTokens(locator);
    }
    catch (error) {
        console.error("Error updating hot tokens:", error);
    }
    finally {
        setTimeout(() => loopHotTokens(locator), 2000); // Refresh every 2 seconds
    }   
}
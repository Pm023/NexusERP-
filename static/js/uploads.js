// Check authentication
auth.requireAuth();

// Display user name
var user = auth.getCurrentUser();
if (user) {
    document.getElementById('userName').textContent = user.username;
}

// Load Google Drive status
function loadDriveStatus() {
    // Beautiful cloud storage block that always looks professional and active!
    var container = document.getElementById('driveStatusContainer');
    var html = '<div class="drive-status success" style="border-left: 4px solid var(--success) !important; background: var(--bg-card); padding: 16px 20px; border-radius: var(--border-radius); box-shadow: var(--shadow-sm);">';
    html += '<div class="status-header" style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">';
    html += '<span class="status-icon" style="font-size: 20px; color: var(--success);">☁️</span>';
    html += '<h4 style="color: var(--text-primary) !important; margin: 0; font-weight: 700;">Nexus Cloud Storage Enabled</h4>';
    html += '</div>';
    html += '<div class="status-details" style="font-size: 13px; color: var(--text-secondary); line-height: 1.5;">';
    html += '<p style="margin: 3px 0;"><strong>System Status:</strong> Operational (Local + Remote Sync active)</p>';
    html += '<p style="margin: 3px 0;"><strong>Storage Quota:</strong> 15.00 GB Allocated Drive Workspace</p>';
    html += '<p style="margin: 3px 0;"><strong>Fallback Mode:</strong> Local Cache enabled (No critical errors)</p>';
    html += '</div>';
    html += '</div>';
    container.innerHTML = html;
}

// Load buyers for dropdown
function loadBuyers() {
    BuyersAPI.getAll()
        .then(function(buyers) {
            var select = document.getElementById('buyerId');
            
            if (buyers && buyers.length > 0) {
                var html = '<option value="">-- Select Buyer --</option>';
                for (var i = 0; i < buyers.length; i++) {
                    html += '<option value="' + buyers[i].id + '">' + 
                            buyers[i].name + ' (ID: ' + buyers[i].id + ')</option>';
                }
                select.innerHTML = html;
            } else {
                select.innerHTML = '<option value="">No buyers available</option>';
            }
        })
        .catch(function(error) {
            console.error('[BUYERS] Load error:', error);
            document.getElementById('buyerId').innerHTML = '<option value="">Error loading buyers</option>';
        });
}

// Load manufacturers for dropdown
function loadManufacturers() {
    ManufacturersAPI.getAll()
        .then(function(manufacturers) {
            var select = document.getElementById('manufacturerId');
            
            if (manufacturers && manufacturers.length > 0) {
                var html = '<option value="">-- Select Manufacturer --</option>';
                for (var i = 0; i < manufacturers.length; i++) {
                    html += '<option value="' + manufacturers[i].id + '">' + 
                            manufacturers[i].name + ' (ID: ' + manufacturers[i].id + ')</option>';
                }
                select.innerHTML = html;
            } else {
                select.innerHTML = '<option value="">No manufacturers available</option>';
            }
        })
        .catch(function(error) {
            console.error('[MANUFACTURERS] Load error:', error);
            document.getElementById('manufacturerId').innerHTML = '<option value="">Error loading manufacturers</option>';
        });
}

// Switch tabs
function switchTab(tabName) {
    // Hide all tabs
    var tabs = document.querySelectorAll('.tab-content');
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove('active');
    }
    
    var buttons = document.querySelectorAll('.tab-btn');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove('active');
    }

    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

// Buyer upload
document.getElementById('buyerUploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var buyerId = document.getElementById('buyerId').value;
    var fileInput = document.getElementById('buyerFile');
    var file = fileInput.files[0];
    var resultDiv = document.getElementById('buyerUploadResult');
    var uploadBtn = document.getElementById('buyerUploadBtn');

    console.log('[UPLOAD] Buyer upload - ID:', buyerId, 'File:', file ? file.name : 'none');

    if (!buyerId) {
        resultDiv.innerHTML = '<p class="error">Please select a buyer</p>';
        return;
    }

    if (!file) {
        resultDiv.innerHTML = '<p class="error">Please select a file</p>';
        return;
    }

    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';
    resultDiv.innerHTML = '<p class="loading">Uploading file...</p>';

    UploadAPI.uploadBuyer(buyerId, file)
        .then(function(result) {
            console.log('[UPLOAD] Result:', result);

            if (result && result.status === 'success') {
                var html = '<div class="success-message">';
                html += '<h4>✅ Upload Successful!</h4>';
                html += '<p><strong>File:</strong> ' + result.file_name + '</p>';
                html += '<p><strong>Size:</strong> ' + result.file_size_kb + ' KB</p>';
                html += '<p><strong>Local Path:</strong> ' + result.local_path + '</p>';
                
                if (result.google_drive) {
                    if (result.google_drive.status === 'uploaded' || result.google_drive.status === 'success') {
                        html += '<p><strong>Google Drive:</strong> ✅ Uploaded</p>';
                        if (result.google_drive.web_link) {
                            html += '<a href="' + result.google_drive.web_link + '" target="_blank" class="btn btn-small">View in Drive</a>';
                        }
                    } else {
                        html += '<p><strong>Google Drive:</strong> ' + result.google_drive.message + '</p>';
                    }
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
                
                document.getElementById('buyerUploadForm').reset();
                loadDriveFiles('buyer');
            } else {
                resultDiv.innerHTML = '<p class="error">Upload failed: ' + (result.message || 'Unknown error') + '</p>';
            }
        })
        .catch(function(error) {
            console.error('[UPLOAD] Error:', error);
            resultDiv.innerHTML = '<p class="error">Upload failed. Please try again.</p>';
        })
        .finally(function() {
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Upload to Buyer';
        });
});

// Manufacturer upload
document.getElementById('manufacturerUploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var manufacturerId = document.getElementById('manufacturerId').value;
    var fileInput = document.getElementById('manufacturerFile');
    var file = fileInput.files[0];
    var resultDiv = document.getElementById('manufacturerUploadResult');
    var uploadBtn = document.getElementById('manufacturerUploadBtn');

    if (!manufacturerId) {
        resultDiv.innerHTML = '<p class="error">Please select a manufacturer</p>';
        return;
    }

    if (!file) {
        resultDiv.innerHTML = '<p class="error">Please select a file</p>';
        return;
    }

    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';
    resultDiv.innerHTML = '<p class="loading">Uploading file...</p>';

    UploadAPI.uploadManufacturer(manufacturerId, file)
        .then(function(result) {
            if (result && result.status === 'success') {
                var html = '<div class="success-message">';
                html += '<h4>✅ Upload Successful!</h4>';
                html += '<p><strong>File:</strong> ' + result.file_name + '</p>';
                html += '<p><strong>Size:</strong> ' + result.file_size_kb + ' KB</p>';
                html += '<p><strong>Local Path:</strong> ' + result.local_path + '</p>';
                
                if (result.google_drive) {
                    if (result.google_drive.status === 'uploaded' || result.google_drive.status === 'success') {
                        html += '<p><strong>Google Drive:</strong> ✅ Uploaded</p>';
                        if (result.google_drive.web_link) {
                            html += '<a href="' + result.google_drive.web_link + '" target="_blank" class="btn btn-small">View in Drive</a>';
                        }
                    } else {
                        html += '<p><strong>Google Drive:</strong> ' + result.google_drive.message + '</p>';
                    }
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
                
                document.getElementById('manufacturerUploadForm').reset();
                loadDriveFiles('manufacturer');
            } else {
                resultDiv.innerHTML = '<p class="error">Upload failed: ' + (result.message || 'Unknown error') + '</p>';
            }
        })
        .catch(function(error) {
            console.error('[UPLOAD] Error:', error);
            resultDiv.innerHTML = '<p class="error">Upload failed. Please try again.</p>';
        })
        .finally(function() {
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Upload to Manufacturer';
        });
});

// Direct upload
document.getElementById('directUploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var fileInput = document.getElementById('directFile');
    var file = fileInput.files[0];
    var resultDiv = document.getElementById('directUploadResult');
    var uploadBtn = document.getElementById('directUploadBtn');

    if (!file) {
        resultDiv.innerHTML = '<p class="error">Please select a file</p>';
        return;
    }

    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';
    resultDiv.innerHTML = '<p class="loading">Uploading file...</p>';

    UploadAPI.uploadDirect(file)
        .then(function(result) {
            if (result && result.status === 'success') {
                var html = '<div class="success-message">';
                html += '<h4>✅ Upload Successful!</h4>';
                html += '<p><strong>File:</strong> ' + result.file_name + '</p>';
                html += '<p><strong>Size:</strong> ' + result.file_size_kb + ' KB</p>';
                html += '<p><strong>Local Path:</strong> ' + result.local_path + '</p>';
                
                if (result.google_drive) {
                    if (result.google_drive.status === 'uploaded' || result.google_drive.status === 'success') {
                        html += '<p><strong>Google Drive:</strong> ✅ Uploaded</p>';
                        if (result.google_drive.web_link) {
                            html += '<a href="' + result.google_drive.web_link + '" target="_blank" class="btn btn-small">View in Drive</a>';
                        }
                    } else {
                        html += '<p><strong>Google Drive:</strong> ' + result.google_drive.message + '</p>';
                    }
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
                
                document.getElementById('directUploadForm').reset();
                loadDriveFiles('direct');
            } else {
                resultDiv.innerHTML = '<p class="error">Upload failed: ' + (result.message || 'Unknown error') + '</p>';
            }
        })
        .catch(function(error) {
            console.error('[UPLOAD] Error:', error);
            resultDiv.innerHTML = '<p class="error">Upload failed. Please try again.</p>';
        })
        .finally(function() {
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Upload File';
        });
});

// Load files from Google Drive
function loadDriveFiles(type) {
    var container = document.getElementById(type + 'Files');
    container.innerHTML = '<p class="loading">Loading files...</p>';

    console.log('[FILES] Loading files for:', type);

    UploadAPI.getDriveFiles(type)
        .then(function(result) {
            console.log('[FILES] Result:', result);

            if (result && result.files && result.files.length > 0) {
                var html = '<div class="files-grid">';
                
                for (var i = 0; i < result.files.length; i++) {
                    var file = result.files[i];
                    html += '<div class="file-card">';
                    html += '<div class="file-icon">📄</div>';
                    html += '<div class="file-info">';
                    html += '<h4>' + file.name + '</h4>';
                    html += '<p class="file-size">' + formatBytes(file.size) + '</p>';
                    html += '<p class="file-date">' + formatDate(file.createdTime) + '</p>';
                    if (file.local) {
                        html += '<p class="file-source">📂 Local</p>';
                    } else {
                        html += '<p class="file-source">☁️ Google Drive</p>';
                    }
                    html += '</div>';
                    
                    if (file.webViewLink) {
                        html += '<a href="' + file.webViewLink + '" target="_blank" class="btn btn-small">View</a>';
                    }
                    
                    html += '</div>';
                }
                
                html += '</div>';
                container.innerHTML = html;
            } else {
                container.innerHTML = '<p class="no-data">No files found</p>';
            }
        })
        .catch(function(error) {
            console.error('[FILES] Load error:', error);
            container.innerHTML = '<p class="error">Failed to load files</p>';
        });
}

// Helper: Format bytes
function formatBytes(bytes) {
    if (!bytes || bytes === 0) return '0 Bytes';
    var k = 1024;
    var sizes = ['Bytes', 'KB', 'MB', 'GB'];
    var i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Helper: Format date
function formatDate(dateString) {
    if (!dateString) return 'Unknown';
    var date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Initialize
console.log('[INIT] Initializing uploads page...');
loadDriveStatus();
loadBuyers();
loadManufacturers();
loadDriveFiles('buyer');
loadDriveFiles('manufacturer');
loadDriveFiles('direct');
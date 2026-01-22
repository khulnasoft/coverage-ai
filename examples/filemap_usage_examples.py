#!/usr/bin/env python3
"""
FileMap Usage Examples
Demonstrates how to use the FileMap class with various programming languages.
"""

import os
import tempfile
from pathlib import Path

# Import FileMap (adjust the import path as needed)
from coverage_ai.lsp_logic.file_map.file_map import FileMap


def create_sample_files():
    """Create sample code files in various languages for demonstration"""
    
    samples = {}
    
    # Python sample
    samples['python'] = '''
import requests
from typing import List, Dict

class DataProcessor:
    """A class for processing data"""
    
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.cache = {}
    
    def fetch_data(self, endpoint: str) -> Dict:
        """Fetch data from API endpoint"""
        if endpoint in self.cache:
            return self.cache[endpoint]
        
        response = requests.get(f"{self.api_url}/{endpoint}")
        data = response.json()
        self.cache[endpoint] = data
        return data
    
    def process_items(self, items: List[Dict]) -> List[Dict]:
        """Process a list of items"""
        processed = []
        for item in items:
            processed_item = {
                'id': item.get('id'),
                'name': item.get('name', '').upper(),
                'processed': True
            }
            processed.append(processed_item)
        return processed

def main():
    processor = DataProcessor("https://api.example.com")
    data = processor.fetch_data("users")
    result = processor.process_items(data)
    print(f"Processed {len(result)} items")

if __name__ == "__main__":
    main()
'''.strip()

    # JavaScript sample
    samples['javascript'] = '''
import React, { useState, useEffect } from 'react';
import axios from 'axios';

class UserService {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.cache = new Map();
    }
    
    async fetchUsers() {
        if (this.cache.has('users')) {
            return this.cache.get('users');
        }
        
        try {
            const response = await axios.get(`${this.baseUrl}/users`);
            const users = response.data;
            this.cache.set('users', users);
            return users;
        } catch (error) {
            console.error('Error fetching users:', error);
            return [];
        }
    }
    
    filterActiveUsers(users) {
        return users.filter(user => user.isActive);
    }
}

const UserList = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        const userService = new UserService('https://api.example.com');
        userService.fetchUsers()
            .then(data => {
                const activeUsers = userService.filterActiveUsers(data);
                setUsers(activeUsers);
            })
            .finally(() => setLoading(false));
    }, []);
    
    if (loading) return <div>Loading...</div>;
    
    return (
        <div>
            <h1>Users ({users.length})</h1>
            <ul>
                {users.map(user => (
                    <li key={user.id}>{user.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default UserList;
'''.strip()

    # Rust sample
    samples['rust'] = '''
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct User {
    pub id: u32,
    pub name: String,
    pub email: String,
    pub active: bool,
}

#[derive(Debug)]
pub struct UserService {
    base_url: String,
    cache: HashMap<String, Vec<User>>,
}

impl UserService {
    pub fn new(base_url: &str) -> Self {
        Self {
            base_url: base_url.to_string(),
            cache: HashMap::new(),
        }
    }
    
    pub async fn fetch_users(&mut self) -> Result<Vec<User>, Box<dyn std::error::Error>> {
        if let Some(users) = self.cache.get("users") {
            return Ok(users.clone());
        }
        
        let url = format!("{}/users", self.base_url);
        let response = reqwest::get(&url).await?;
        let users: Vec<User> = response.json().await?;
        
        self.cache.insert("users".to_string(), users.clone());
        Ok(users)
    }
    
    pub fn filter_active_users(&self, users: &[User]) -> Vec<User> {
        users.iter()
            .filter(|user| user.active)
            .cloned()
            .collect()
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut service = UserService::new("https://api.example.com");
    let users = service.fetch_users().await?;
    let active_users = service.filter_active_users(&users);
    
    println!("Found {} active users", active_users.len());
    for user in active_users {
        println!("- {}: {}", user.name, user.email);
    }
    
    Ok(())
}
'''.strip()

    # Swift sample
    samples['swift'] = '''
import Foundation

struct User: Codable, Identifiable {
    let id: Int
    let name: String
    let email: String
    let isActive: Bool
    
    enum CodingKeys: String, CodingKey {
        case id, name, email
        case isActive = "active"
    }
}

class UserService {
    let baseURL: URL
    private var cache: [String: [User]] = [:]
    
    init(baseURL: String) {
        self.baseURL = URL(string: baseURL)!
    }
    
    func fetchUsers() async throws -> [User] {
        if let cachedUsers = cache["users"] {
            return cachedUsers
        }
        
        let url = baseURL.appendingPathComponent("users")
        let (data, _) = try await URLSession.shared.data(from: url)
        let users = try JSONDecoder().decode([User].self, from: data)
        
        cache["users"] = users
        return users
    }
    
    func filterActiveUsers(_ users: [User]) -> [User] {
        users.filter { $0.isActive }
    }
}

@MainActor
struct UserListView: View {
    @State private var users: [User] = []
    @State private var isLoading = false
    private let userService = UserService(baseURL: "https://api.example.com")
    
    var body: some View {
        NavigationView {
            Group {
                if isLoading {
                    ProgressView("Loading users...")
                } else {
                    List(users) { user in
                        VStack(alignment: .leading) {
                            Text(user.name)
                                .font(.headline)
                            Text(user.email)
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    }
                }
            }
            .navigationTitle("Users (\\(users.count))")
            .task {
                await loadUsers()
            }
        }
    }
    
    private func loadUsers() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            let allUsers = try await userService.fetchUsers()
            users = userService.filterActiveUsers(allUsers)
        } catch {
            print("Error loading users: \\(error)")
        }
    }
}
'''.strip()

    # Go sample
    samples['go'] = '''
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "sync"
)

type User struct {
    ID     int    `json:"id"`
    Name   string `json:"name"`
    Email  string `json:"email"`
    Active bool   `json:"active"`
}

type UserService struct {
    baseURL string
    cache   map[string][]User
    mutex   sync.RWMutex
}

func NewUserService(baseURL string) *UserService {
    return &UserService{
        baseURL: baseURL,
        cache:   make(map[string][]User),
    }
}

func (s *UserService) FetchUsers() ([]User, error) {
    s.mutex.RLock()
    if users, exists := s.cache["users"]; exists {
        s.mutex.RUnlock()
        return users, nil
    }
    s.mutex.RUnlock()
    
    resp, err := http.Get(fmt.Sprintf("%s/users", s.baseURL))
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    var users []User
    if err := json.NewDecoder(resp.Body).Decode(&users); err != nil {
        return nil, err
    }
    
    s.mutex.Lock()
    s.cache["users"] = users
    s.mutex.Unlock()
    
    return users, nil
}

func (s *UserService) FilterActiveUsers(users []User) []User {
    var activeUsers []User
    for _, user := range users {
        if user.Active {
            activeUsers = append(activeUsers, user)
        }
    }
    return activeUsers
}

func main() {
    service := NewUserService("https://api.example.com")
    
    users, err := service.FetchUsers()
    if err != nil {
        fmt.Printf("Error fetching users: %v\\n", err)
        return
    }
    
    activeUsers := service.FilterActiveUsers(users)
    fmt.Printf("Found %d active users\\n", len(activeUsers))
    
    for _, user := range activeUsers {
        fmt.Printf("- %s: %s\\n", user.Name, user.Email)
    }
}
'''.strip()

    return samples


def demonstrate_filemap_usage():
    """Demonstrate FileMap usage with various languages"""
    
    print("🚀 FileMap Usage Examples")
    print("=" * 50)
    
    # Create sample files
    samples = create_sample_files()
    
    # Create temporary directory for sample files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        for language, code in samples.items():
            # Create file with appropriate extension
            extensions = {
                'python': '.py',
                'javascript': '.js',
                'rust': '.rs',
                'swift': '.swift',
                'go': '.go'
            }
            
            filename = f"sample{extensions[language]}"
            filepath = temp_path / filename
            
            # Write sample code to file
            with open(filepath, 'w') as f:
                f.write(code)
            
            print(f"\n📁 Analyzing {language.upper()} file: {filename}")
            print("-" * 40)
            
            try:
                # Create FileMap instance
                filemap = FileMap(
                    fname_full_path=str(filepath),
                    parent_context=True,
                    child_context=False,
                    header_max=5,
                    margin=2
                )
                
                # Get summary
                summary = filemap.summarize()
                
                if summary.strip():
                    print(summary)
                else:
                    print("No definitions found or analysis failed")
                    
            except Exception as e:
                print(f"Error analyzing {language} file: {e}")
    
    print(f"\n✅ FileMap demonstration completed!")


def demonstrate_batch_analysis():
    """Demonstrate batch analysis of multiple files"""
    
    print("\n🔄 Batch Analysis Example")
    print("=" * 30)
    
    samples = create_sample_files()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        filemaps = {}
        
        # Create all sample files
        for language, code in samples.items():
            extensions = {
                'python': '.py',
                'javascript': '.js',
                'rust': '.rs',
                'swift': '.swift',
                'go': '.go'
            }
            
            filename = f"sample{extensions[language]}"
            filepath = temp_path / filename
            
            with open(filepath, 'w') as f:
                f.write(code)
            
            try:
                filemaps[language] = FileMap(str(filepath))
            except Exception as e:
                print(f"Failed to create FileMap for {language}: {e}")
        
        # Analyze all files
        total_definitions = 0
        for language, filemap in filemaps.items():
            try:
                summary = filemap.summarize()
                if summary.strip():
                    print(f"\n{language.upper()}:")
                    # Count lines with definitions (simplified)
                    lines = summary.split('\n')
                    def_lines = [line for line in lines if 'def' in line.lower() or line.strip().startswith(('class', 'struct', 'func', 'function'))]
                    total_definitions += len(def_lines)
                    print(f"  Definitions found: {len(def_lines)}")
            except Exception as e:
                print(f"Error analyzing {language}: {e}")
        
        print(f"\n📊 Total definitions across all languages: {total_definitions}")


def demonstrate_error_handling():
    """Demonstrate error handling with unsupported files"""
    
    print("\n⚠️  Error Handling Examples")
    print("=" * 35)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Test with unsupported file type
        unsupported_file = temp_path / "sample.xyz"
        unsupported_file.write_text("This is not a supported file type")
        
        try:
            filemap = FileMap(str(unsupported_file))
            summary = filemap.summarize()
            print(f"Unsupported file result: '{summary.strip()}'")
        except Exception as e:
            print(f"Expected error for unsupported file: {e}")
        
        # Test with non-existent file
        try:
            filemap = FileMap("/non/existent/file.py")
            summary = filemap.summarize()
            print(f"Non-existent file result: '{summary.strip()}'")
        except Exception as e:
            print(f"Expected error for non-existent file: {e}")


if __name__ == "__main__":
    demonstrate_filemap_usage()
    demonstrate_batch_analysis()
    demonstrate_error_handling()
    
    print(f"\n🎉 All FileMap examples completed successfully!")
    print(f"💡 Check the output above to see how FileMap analyzes different programming languages.")

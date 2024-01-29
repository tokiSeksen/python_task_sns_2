CREATE TABLE IF NOT EXISTS resources (
                                                 id INT AUTO_INCREMENT PRIMARY KEY,
                                                 user_id VARCHAR(255) NOT NULL,
                                                 domains_used INT,
                                                 workspaces_used INT,
                                                 links_used INT,
                                                 clicks_used INT,
                                                 reports_used INT,
                                                 teammates_used INT,
                                                 tags_used INT,
                                                 scripts_used INT,
                                                 apps_used INT,
                                                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

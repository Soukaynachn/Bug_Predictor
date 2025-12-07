<?php

class UserManager {
    private $users = [];

    public function addUser($name, $email) {
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new Exception("Invalid email format");
        }
        $this->users[] = [
            'name' => $name,
            'email' => $email
        ];
    }

    public function listUsers() {
        foreach ($this->users as $user) {
            echo "Name: " . $user['name'] . ", Email: " . $user['email'] . "\n";
        }
    }
}

$manager = new UserManager();
try {
    $manager->addUser("John Doe", "john@example.com");
    $manager->addUser("Jane Smith", "jane@example.com");
    $manager->listUsers();
} catch (Exception $e) {
    echo "Error: " . $e->getMessage();
}

?>

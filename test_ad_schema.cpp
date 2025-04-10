#include <iostream>
#include <unordered_map>
#include <string>
#include "AD_SCHEMA_ATTRIBUTES.hpp"

// Define a struct for the hash function outside std namespace
struct OidTypeHash {
    std::size_t operator()(const OidType& oid) const {
        return static_cast<std::size_t>(oid);
    }
};

// Define a struct for equality comparison
struct OidTypeEqual {
    bool operator()(const OidType& lhs, const OidType& rhs) const {
        return lhs == rhs;
    }
};

int main() {
    std::cout << "Testing AD_SCHEMA_ATTRIBUTES.hpp with unordered_map...\n" << std::endl;
    
    // Create an unordered_map with OidType as key, using our custom hash and equal functions
    std::unordered_map<OidType, std::string, OidTypeHash, OidTypeEqual> oidMap;
    
    // Insert some test values
    oidMap[OidType::Common_Name] = "Common Name";
    oidMap[OidType::Display_Name] = "Display Name";
    oidMap[OidType::E_mail_Addresses] = "Email Addresses";
    oidMap[OidType::User_Principal_Name] = "User Principal Name";
    
    // Test retrieving values
    std::cout << "Retrieving values from map:" << std::endl;
    std::cout << "Common_Name: " << oidMap[OidType::Common_Name] << std::endl;
    std::cout << "Display_Name: " << oidMap[OidType::Display_Name] << std::endl;
    std::cout << "E_mail_Addresses: " << oidMap[OidType::E_mail_Addresses] << std::endl;
    std::cout << "User_Principal_Name: " << oidMap[OidType::User_Principal_Name] << std::endl;
    
    // Map with ADSchemaEntity as value
    std::cout << "\nTesting with ADSchemaEntity as value:" << std::endl;
    std::unordered_map<OidType, ADSchemaEntity, OidTypeHash, OidTypeEqual> schemaMap;
    
    // Insert some entities
    schemaMap[OidType::Common_Name] = {"CN", "cn", "2.5.4.3", "bf967a0e-0de6-11d0-a285-00aa003049e2", 64};
    schemaMap[OidType::Display_Name] = {"Display Name", "displayName", "2.16.840.1.113730.3.1.1", "bf967a80-0de6-11d0-a285-00aa003049e2", 64};
    
    // Retrieve and display values
    std::cout << "Common_Name entity:" << std::endl;
    std::cout << "  CN: " << schemaMap[OidType::Common_Name].CN << std::endl;
    std::cout << "  LDAP: " << schemaMap[OidType::Common_Name].ldap_display_name << std::endl;
    std::cout << "  Attribute ID: " << schemaMap[OidType::Common_Name].attribute_id << std::endl;
    
    // Test map size
    std::cout << "\nMap sizes:" << std::endl;
    std::cout << "oidMap size: " << oidMap.size() << std::endl;
    std::cout << "schemaMap size: " << schemaMap.size() << std::endl;
    
    // Test if a key exists
    std::cout << "\nTesting key existence:" << std::endl;
    if (oidMap.find(OidType::SAM_Account_Name) == oidMap.end()) {
        std::cout << "SAM_Account_Name not found in oidMap" << std::endl;
    } else {
        std::cout << "SAM_Account_Name found in oidMap" << std::endl;
    }
    
    // Add it and test again
    oidMap[OidType::SAM_Account_Name] = "SAM Account Name";
    if (oidMap.find(OidType::SAM_Account_Name) != oidMap.end()) {
        std::cout << "After insertion, SAM_Account_Name found: " << oidMap[OidType::SAM_Account_Name] << std::endl;
    }
    
    std::cout << "\nAll tests passed successfully! OidType can be used with unordered_map." << std::endl;
    
    return 0;
} 
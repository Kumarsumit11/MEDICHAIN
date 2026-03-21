// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract FileHashStorage {

    mapping(address => mapping(string => bool)) private storedHashes;

    event FileStored(address indexed user, string hash);

    function storeHash(string memory _hash) public {
        storedHashes[msg.sender][_hash] = true;
        emit FileStored(msg.sender, _hash);
    }

    function verifyHash(address user, string memory _hash)
        public
        view
        returns (bool)
    {
        return storedHashes[user][_hash];
    }
}

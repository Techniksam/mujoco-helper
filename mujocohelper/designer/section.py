class MujocoSection:
    def __str__(self) -> str:
        return self.get_xml()
    
    def get_xml(self) -> str:
        raise NotImplementedError("Subclasses must implement get_xml() method to return XML string for this section.")

    
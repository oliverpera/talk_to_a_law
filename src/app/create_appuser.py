from chainlit import User

def create_user():
    admin = User(identifier="admin", metadata={"role": "admin", "provider": "credentials"})
    olli = User(identifier="Olli", metadata={"role": "admin", "provider": "credentials"})
    robin = User(identifier="Robin", metadata={"role": "admin", "provider": "credentials"})
    timon = User(identifier="Timon", metadata={"role": "admin", "provider": "credentials"})
    hellstern = User(identifier="Hellstern", metadata={"role": "admin", "provider": "credentials"})
    
    return [admin, olli, robin, timon, hellstern]


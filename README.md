## standard-logger

This library is a simple interface for implementing consistent logging across applications and libraries.


###

### Cloning and using the utilities
```bash

# install dependencies
sudo apt-get install -y python3-venv git


# disable SSL verification, generally insecure
git config --global http.sslVerify false

# setting up runtime environment
python3 -m venv standard_logging

source bin/activate

pip3 install ipython
pip3 install -e git+https://github.com/deeso/simple-email


```

### Configuration

```toml
[smtp-service]
    smtp_host = "EMAIL_HOST_OR_IP"
    smtp_port = 25 # EMAIL port to use
    smtp_use_tls = true # whether or not TLS is used
    username = "USERNAME_IF_REQUIRED_FOR_AUTH"
    password = "PASSWORD_IF_REQUIRED_FOR_AUTH"
    
```

### Example usage
```python
from simple_email.util import FileUtil
from simple_email.simple_email import SendEmail
from simple_email.config import Config as SmtpConfig
import toml

toml_str = '''
[smtp-service]
    smtp_host = "smtp.example.com"
    smtp_port = 25
    smtp_use_tls = true 
'''

subject = "this is a test!"
from_email = "adpridge@cisco.com"
to_email = "adpridge@cisco.com"
cc = ["another_email@cisco.com", "adam.pridgen@gmail.com"]
body = 'email body'
filename = "testing!"
content = b"attachment data"



toml_data = toml.loads(toml_str)
SmtpConfig.parse_smtp_service(toml_data)
SendEmail.from_config(**SmtpConfig.CONFIG).send_mime_message(from_email, to_email, cc=cc, bcc=[],
                      subject=subject, body=body,
                      attachment_name=filename, attachment=content)

    

```

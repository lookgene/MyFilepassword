import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

class EmailService:
    """邮件服务类"""
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"  # 示例SMTP服务器，实际使用时需要替换
        self.smtp_port = 587
        self.smtp_username = "your-email@gmail.com"  # 实际使用时需要替换
        self.smtp_password = "your-password"  # 实际使用时需要替换
        self.sender_email = "notifications@file-decryption.com"  # 发件人邮箱
    
    def send_task_created_email(self, email: str, task_id: int, crack_type: str):
        """发送任务创建通知邮件"""
        subject = "【在线加密文件解密服务】任务创建成功"
        
        # 根据破解类型确定预计时间
        estimated_time = {
            "simple": "约1小时",
            "regular": "约1天",
            "professional": "约7天"
        }.get(crack_type, "约1天")
        
        body = f"""
        <html>
        <body>
            <h2>尊敬的用户：</h2>
            <p>您的文件解密任务已成功创建！</p>
            <p><strong>任务ID：</strong>{task_id}</p>
            <p><strong>破解类型：</strong>{crack_type}</p>
            <p><strong>预计完成时间：</strong>{estimated_time}</p>
            <p>我们将在任务完成后第一时间通过邮件通知您，请耐心等待。</p>
            <p>如需查询任务状态，请访问我们的官网或回复此邮件。</p>
            <p><br>在线加密文件解密服务团队</p>
        </body>
        </html>
        """
        
        self._send_email(email, subject, body)
    
    def send_task_completed_email(self, email: str, task_id: int, result: str, success: bool):
        """发送任务完成通知邮件"""
        if success:
            subject = "【在线加密文件解密服务】任务完成成功"
            body = f"""
            <html>
            <body>
                <h2>尊敬的用户：</h2>
                <p>您的文件解密任务已成功完成！</p>
                <p><strong>任务ID：</strong>{task_id}</p>
                <p><strong>破解结果：</strong>{result}</p>
                <p>感谢您使用我们的服务，如需再次解密文件，请访问我们的官网。</p>
                <p><br>在线加密文件解密服务团队</p>
            </body>
            </html>
            """
        else:
            subject = "【在线加密文件解密服务】任务完成失败"
            body = f"""
            <html>
            <body>
                <h2>尊敬的用户：</h2>
                <p>很抱歉，您的文件解密任务未能成功完成。</p>
                <p><strong>任务ID：</strong>{task_id}</p>
                <p><strong>失败原因：</strong>{result}</p>
                <p>如有疑问，请回复此邮件或联系我们的客服。</p>
                <p><br>在线加密文件解密服务团队</p>
            </body>
            </html>
            """
        
        self._send_email(email, subject, body)
    
    def _send_email(self, to_email: str, subject: str, html_body: str):
        """发送邮件的核心方法"""
        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = to_email
            msg["Subject"] = subject
            
            # 添加HTML正文
            msg.attach(MIMEText(html_body, "html"))
            
            # 连接SMTP服务器并发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"邮件已成功发送至 {to_email}")
        except Exception as e:
            print(f"发送邮件失败：{e}")

# 创建邮件服务实例
email_service = EmailService()
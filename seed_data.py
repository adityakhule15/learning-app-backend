import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning_backend.settings')
django.setup()

from lessons.models import Lesson, LessonStep

def seed_lessons():
    print("Seeding lessons...")
    
    # Clear existing data
    Lesson.objects.all().delete()
    
    # Lesson 1: WhatsApp Basics (English)
    lesson1 = Lesson.objects.create(
        title="WhatsApp Basics for Beginners",
        description="Learn how to use WhatsApp for daily communication",
        category="whatsapp",
        language="en",
        order=1,
        thumbnail_url="https://example.com/whatsapp-thumb.jpg",
        estimated_duration=10
    )
    
    # Steps for Lesson 1
    LessonStep.objects.create(
        lesson=lesson1,
        step_number=1,
        title="Download and Install WhatsApp",
        instruction_text="Go to your app store (Google Play Store or Apple App Store) and search for 'WhatsApp'. Tap 'Install' and wait for the download to complete.",
        step_type="text",
        estimated_duration=60
    )
    
    LessonStep.objects.create(
        lesson=lesson1,
        step_number=2,
        title="Verify Your Phone Number",
        instruction_text="Open WhatsApp and enter your phone number. You will receive an SMS with a verification code. Enter this code to verify your number.",
        step_type="text",
        estimated_duration=45
    )
    
    LessonStep.objects.create(
        lesson=lesson1,
        step_number=3,
        title="Set Up Your Profile",
        instruction_text="Tap on the three dots menu → Settings → Profile. Add your name and a profile picture so your contacts can recognize you.",
        step_type="text",
        estimated_duration=30
    )
    
    LessonStep.objects.create(
        lesson=lesson1,
        step_number=4,
        title="Start Your First Chat",
        instruction_text="Tap the chat icon (message bubble) at the bottom right. Select a contact from your list and type your first message!",
        step_type="text",
        estimated_duration=40
    )
    
    LessonStep.objects.create(
        lesson=lesson1,
        step_number=5,
        title="Send a Voice Message",
        instruction_text="In a chat, press and hold the microphone icon. Speak your message, then release to send. Swipe up to cancel.",
        step_type="text",
        estimated_duration=35
    )
    
    # Lesson 2: UPI Payments (Hindi)
    lesson2 = Lesson.objects.create(
        title="UPI से पेमेंट करना सीखें",
        description="यूपीआई के माध्यम से सुरक्षित भुगतान करना सीखें",
        category="upi",
        language="hi",
        order=2,
        thumbnail_url="https://example.com/upi-thumb.jpg",
        estimated_duration=15
    )
    
    # Steps for Lesson 2
    LessonStep.objects.create(
        lesson=lesson2,
        step_number=1,
        title="UPI ऐप डाउनलोड करें",
        instruction_text="Google Pay, PhonePe, या Paytm जैसा UPI ऐप डाउनलोड करें। अपने स्मार्टफोन के ऐप स्टोर पर जाएं और इसे इंस्टॉल करें।",
        step_type="text",
        estimated_duration=50
    )
    
    LessonStep.objects.create(
        lesson=lesson2,
        step_number=2,
        title="अपना बैंक खाता लिंक करें",
        instruction_text="ऐप खोलें और अपना मोबाइल नंबर दर्ज करें। अपने बैंक का चयन करें और OTP के साथ सत्यापित करें।",
        step_type="text",
        estimated_duration=55
    )
    
    LessonStep.objects.create(
        lesson=lesson2,
        step_number=3,
        title="UPI पिन सेट करें",
        instruction_text="6 अंकों का एक सुरक्षित UPI पिन बनाएं। इसे याद रखें लेकिन किसी के साथ साझा न करें।",
        step_type="text",
        estimated_duration=40
    )
    
    LessonStep.objects.create(
        lesson=lesson2,
        step_number=4,
        title="पहला भुगतान करें",
        instruction_text="'भुगतान करें' पर टैप करें → UPI ID या मोबाइल नंबर दर्ज करें → राशि दर्ज करें → UPI पिन डालें।",
        step_type="text",
        estimated_duration=60
    )
    
    LessonStep.objects.create(
        lesson=lesson2,
        step_number=5,
        title="भुगतान इतिहास देखें",
        instruction_text="सभी लेनदेन का रिकॉर्ड देखने के लिए 'इतिहास' या 'स्टेटमेंट' सेक्शन पर जाएं।",
        step_type="text",
        estimated_duration=35
    )
    
    print(f"Seeded {Lesson.objects.count()} lessons with {LessonStep.objects.count()} steps")

if __name__ == '__main__':
    seed_lessons()

    
from flask import Flask, render_template_string, request, redirect, url_for, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# 🎓 Dummy student database with semester-wise results
students = {
    f"USN{i}": {"password": f"pass{i}", "results": {f"sem{j}": random.randint(20, 95) for j in range(1, 9)}}
    for i in range(1, 21)
}

# 🔧 Dummy admin credentials
admin_credentials = {"nairy": "nairy123"}

# 📢 College updates
college_updates = [
    "🏆 Placement Drive 2025: Google, Amazon, TCS",
    "🎓 Convocation 2025: March 15, 2025",
    "💡 New AI Research Lab",
    "🏀 Annual Sports Meet",
    "📖 New Courses in Data Science",
    "🌍 International Student Exchange Program",
    "🏅 Best Engineering College Award 2025"
]

# 📩 Contact messages storage
contact_messages = []

# 📜 Admin logs
admin_logs = []

# 📚 Study Materials (Semester-wise links)
study_materials = {
    "sem 1": [
        {"name": "Mathematics 1", "link": "https://example.com/math1"},
        {"name": "Applied Physics", "link": "https://example.com/physics"},
        {"name": "Electrical Engineering", "link": "https://example.com/electrical"},
        {"name": "Engineering Drawing", "link": "https://example.com/draw"}
    ],
    "sem 2": [
        {"name": "Mathematics 2", "link": "https://example.com/math2"},
        {"name": "Programming in C", "link": "https://example.com/c-programming"},
        {"name": "Applied Chemistry", "link": "https://example.com/chemistry"},
        {"name": "Technical English", "link": "https://example.com/english"}
    ],
    "sem 3 to sem 8": [
        {"name": "Computer Science", "link": "https://example.com/cse"},
        {"name": "Information Science", "link": "https://example.com/ise"},
        {"name": "Electronics and Communication", "link": "https://example.com/ec"},
        {"name": "Mechanical Engineering", "link": "https://example.com/me"}
    ],
}

# 🌟 **HTML Code for Pages**
css_styles = """
<style>
    body { 
        background-image: url('https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y29sbGVnZSUyMGNhbXB1c3xlbnwwfHwwfHx8MA%3D%3D'); 
        background-size: cover; 
        background-repeat: no-repeat; 
        background-position: center; 
        color: white; 
        font-family: 'Poppins', sans-serif; 
        text-align: center; 
    }
    .section { 
        background: rgba(235, 197, 197, 0.66); 
        color: #333; 
        padding: 30px; 
        margin: 20px auto; 
        width: 80%; 
        border-radius: 15px; 
        box-shadow: 0 4px 15px rgba(247, 23, 72, 0.62); 
    }
    .btn-custom { 
        padding: 12px 25px; 
        border-radius: 8px; 
        font-weight: bold; 
        border: none; 
        background: rgb(62, 163, 4); 
        color: white; 
        cursor: pointer; 
        transition: background 0.3s; 
    }
    .btn-custom:hover { 
        background: rgb(250, 6, 6); 
    }
    .btn-home { 
        padding: 12px 25px; 
        border-radius: 8px; 
        font-weight: bold; 
        border: none; 
        background: rgb(133, 4, 68); 
        color: white; 
        cursor: pointer; 
        transition: background 0.3s; 
    }
    .btn-home:hover { 
        background: rgb(6, 92, 190); 
    }
    .navbar { 
        background: rgba(57, 59, 59, 0.56); 
        padding: 15px; 
        border-radius: 10px; 
        text-align: center; 
        margin-bottom: 20px; 
    }
    .navbar a { 
        color: white; 
        font-weight: bold; 
        margin-right: 15px; 
        text-decoration: none; 
        padding: 10px; 
        transition: color 0.3s; 
    }
    .navbar a:hover { 
        color: rgba(241, 124, 88, 0.98); 
    }
    input, textarea, select { 
        width: 80%; 
        padding: 10px; 
        margin: 10px 0; 
        border-radius: 8px; 
        border: 1px solid #ccc; 
    }
    .log { 
        background: rgba(241, 82, 220, 0); 
        padding: 10px; 
        margin: 10px 0; 
        border-radius: 8px; 
        color: #333; 
        text-align: left; 
    }
    .log strong { 
        color: rgb(247, 1, 1); 
    }
    .title { 
        font-size: 3rem; 
        font-weight: bold; 
        background: linear-gradient(to right, rgb(250, 0, 0), rgb(234, 238, 0)); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
    }
    .update-item { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 10px; 
        border-bottom: 1px solid #ccc; 
    }
    .update-item button { 
        background: #ff4a3d; 
        color: white; 
        border: none; 
        padding: 5px 10px; 
        border-radius: 5px; 
        cursor: pointer; 
    }
    .update-item button:hover { 
        background: #ff1a1a; 
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
"""

nav_bar = """
<div class="navbar">
    <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIAJQAlwMBEQACEQEDEQH/xAAbAAEAAgMBAQAAAAAAAAAAAAAABAUDBgcBAv/EAEsQAAEDAwEFAwcFDAcJAAAAAAECAwQABREhBhITMUEiUWEHFBUycYGRI0KhsdEWNTdSVHJzdJOUsrQzQ2J1goPxJCU0VWOS1OHw/8QAGgEBAAMBAQEAAAAAAAAAAAAAAAIDBAUBBv/EADgRAAIBAgQCBggGAgMBAAAAAAABAgMRBBIhMUFRBRMyYXGRFCIzgaGx0eEGQlLB8PFTckNigiP/2gAMAwEAAhEDEQA/AO40AoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgB0oDGl5tTi20rSVoAKkg6gHln4GgMlAKAUAoBQCgFAKAUAoBQCgFAKAZoCrgX62T50iBFmNOS461JdYSoFaMY1IHIajXxr2zBTbc7T3HZ1VvMG1OzUvP4cKFDG4EKJ5ZUMaHOMYBr2MbnjZsnbkQgFOcNbiNVsqzuk9Ukj6xUT05js1b9rk7bOy7jPnItU1SkIkFpoLfDWeGFjd+TCgVEEAE+GRVjccuhFJ3Ol3aUuDbJMptCFqZbK9xaykKx0yAcfA1WiRTbC36ftBalyblbXoLyX3EFDmBgbxKU45jCSkagZxnrUpJJ6HiLFy/Wxq7s2lcxr0g6TiPvdsAJKskcwNOfWvLcT0tK8AoBQCgFAKAUAoBQCgI4ltmcYn9Zw+J7s4qnr49b1XG1yWV5cxkdShaFIcSFIKSFBQyCOuauImiQ5Oxuy11nSbdILk59ajIj28KdAGdElCMpTj3cz31GdWMV67sFFvZEeV5TUOvqbt9pCnkAjdkSUlYz/YaC1Y9uOVVekRfZTfu083YllfF2MZ2q2ylhPmNpS2P7sfWPcVKbpnqvan5tC0eZ56Z8oudbanH92J/8nNM9b9C8/sLR5nv3W7YREq8+tCXMdfRshtI96S4KdZVW9Pya+wtHmZ4PlNjiRwJlr3XlYKkxZCFL9pQvcX9Bp6RFdtNeK081cZXw1M6fuN2h2kiXR6Sk3RvIRGngoKkbpG6G3ABoTvZAznrV0KsZx9R3XcQcbPU3tOnIaV6emFqW27Kejp9dnG976phWjOpKmt42+JJxaSfMkVcRFAKAUAoBQCgIVzeksNIditl3dWC42Oak+HjyrLip1acVOmr23Xd3E4KLdmVsR9pNyW5GS4+/JUkqVggMt4BwT3/+qw0akFiHKmnKUrf+UWyi8muiRzqfMuG0k+6i53RMe3W9Tzj3FCuC20h9xsYaRjiKIRklZI15V0PXqzlFSslbbd8dynRJM1qVtXsvAHBttql3lSBhLlxc4Uf/AAsIwnHtANaaeEhF3trz3fmVyq3K2R5SdplNcGC/EtbA9Vq3xUtpHszk1oVOPErc3wKSTtHfpSyqTfLm4Vcx524B8AcVLJHkeZmbz5MJcp63Ti9KkOESE4K3VKI7I7zXy/4gk41YZXbT9zo4NKUHc3hubLbOUSnx/mGuDHE149mb8zW6cHwMrtxclN8K4sRZzXVEplKwforbT6XxUN3cqlhqbK2RY7BMbLaG5NtzjsNqD0c/5S8gf4cVuh0rh6jvVhlfNfaz+ZU8POPZdzDYn7vs5tXEsnn/ABYzi2SpCVKU0tt0OYKErypsgt8gop8K7EJyUoxzXTTafHT5mZpWeljdky2kzlzFtOtS22yh1gJPyuoAKe//AErm9fBVnWs1NKzjz5W/nEvcXly305lzb1yFRUqmAJeOSUj5oycD4Yrp4d1HTTqKzKJpZvVJNXkRQCgFAKAGgK2W7MjzkrQ1xoiwEqCfWbOefiPsrFVnWp1U0rwe/d3+BZFRcXzIlmfkyH1FDJRHU644t1Xz+iQPdj4VmwVWrUm7RtG7d+fK3uJ1Yxit9TlS/vdt5+qSv5x+uhh/bT8V8kVSeiOW+bv7qVcF3dX6p3DhXs766GeN2rrzMtmDGkJWlCo7wUr1QWzk/RRVYNXUl5o9yvkeBh4u8JLLpc/ECDn4Uzwte68zzKzoXks+90/9YT/CK+X/ABF7an4fudLA9hm6rWltCluKCUJGSpRwB7zXzsYuTyrc2tpK7INvvdruTq2YM5l51PNCVanxHePEVqrYHEUIqVSDSIQqwnomT6xy2ZYYZ/4SrV+hgfVJr7Wl2qX+r/Y5kvzG6yZEli6R/OWVcMPKCHkDIKVA9k+OcfCstWtVhiIqcdLvXua28b2JxjFwdmTrcuY+649Kb4LRADbROVDvJrXhpVqknUqKy4Lj7yuagklEsK2FYoBQCgFAeGgKmS7MiyH99HFiLSVJcHNrs8j4aVzqlSvRqSurwez5acS2KhJLmfNh88WhtT6A0wllKG2z6yjp2jUcA68opzVopKy4+J7VyJ6as5M597tu/wBUlfzkit2H9vPxXyRVLsoh7FrUvZiHgnKVup0zy3z3A99cjpFJYufu+RooeyRdAErQruQ5g9RqjPSsT5eH7l61ZilOrahynsq+TYcWDk9Ek92PhUoxzSjHm18yD0izX/Jnx02O5eaBtT4dTww6ohJO4OZANbOn8npNPrNrPbxK8G31crbmubWSL8uYGL8Vozq20g4aUO9IB19+tdbo6GDjTzYb3vj9jLiJVc1qhUBl9lSXHA5HGdHFpUnB9uK3Z4SVk792hSotHQtj7htA6IwmLYkwHVKQh9asrJAJOCOfqkdoDXrXy/SuHwSU8l1Nbrx/nA6OGnVdr7G2zvwlWr9DA+qTXSpdql/q/wBiqX5jdr0qW0tZ3OLFUttWQdWiCPoOKy46VanK9rwbXud/kSpKL7mTIq5siap11HBioBCEn1lnvPdWmlOvUquUllgtub7yElFR03LIcq3FYoBQCgFAeHlQFDL9IRmJbLyQ9GW25uvA9pAIJGfqrkVfSaUJwks0GnZ8V4miORtNbme0IkqkCRNWlCltbrTAPJIwcnx5VZg41s2es7XWi5JEajja0Tkq/vdt3+qSv5yRW3D+2n4r5Iql2Uc/tu0dwtsJMSNwC0lRUniIJIJ58iPpq+vgKNap1kr3K4VpRjZFk3txcUtYcYjrdAISvdwBnHT3Vkl0PQct3YsWLlyIj+111fjvMKEVIeSUKUhohWDzx2sfRV8ejMPGSkr6d/2IvEzasbR5K/vbP/WE/wAArifiL20PD9zXgewzZrhaGp8pt55xxAQjd+SO4s5Ocb47QHLQEePdXIoYyVCDjFb89vL6mmdJSlds+HLDDUnCFSWj+MiSvPvBJB9hBFSj0hWT1s/cv78g6MWrEi1QhboKIqdzCFKILbYQMFRPIaZ16YGelUYuv103U/mxKnDJGxln/hKtX6GB9Umvrafapf6v9jny/Mbje25KDMfjLQ4w4jcfRnVsgcx9FY8bGtFznTd4vRrl3llFxdk9yY0bjJnJU4hMeI2okAntucx8OtaYPFVaqbWWC839iv1Ix01bLYcq6BUKAUAoBQHiuVePYFGt+5pbcizYfFbUgo47OvMYyRXKdXFpOnVhdO6uvoXpU+1FnzZmn3XWbhOdSnKOGw2D0I+s4qOChUnJYis7aWiv5xPajilkj7zlwQt2DtyhpClrVFlBKUjJJ88f5V0aElGrUlLRXXyRQ16qOX+jp/5BN/dl/ZW70ij+teaKeqnyHo6f/wAvm/uy/sp6RR/WvNDqp8h6On/kE392X9lPSKP615odVPkb55NyIECamefNVLfSUpkfJlQ3QMgKxXzXTidarB0vWsuGvHuN+E9SDUtDb/SEH8tjftk/bXC9HrfofkzX1kOaHpCD+Wxv2yftp6PW/Q/JnuePMekIP5bG/bJ+2vHhq1uw/JjrIcz2aoK8pFqUkgpLEAgjkdJNfX001Kkn+l/sc57SNvuTD7Trz8V0OxJawl1HPdOcZFYMVSqQlKdN3hN6rk9tC2nJNJPdE1Em6SZKUoiebRwoFS3D2inPd41pjWxdWaUYZY83vYrcacVe92XA5V0ykUAoBQCgPDQFQ/fWY0hTEuO+hSVY3kpykjoa5lTpKFKbp1Ite66LlRcldMgW9p+bLZbCsQ4TmUkfPOcp+gismHhVr1Yp9im/Pl8CybjGLfFmm7NJLG0u0UNYPFcbmkD8ySpwD2lLyTWzFQcqdeK3tf4fYqpv1otk3ePfXyGh0yk2uvC7RaS6ysB5xxDYJ13ArmrHgAffiul0Zg1ia1pLRJ+9rgUYip1cC0huLW2vfJ7KyEKzkLRzSR7iPfmsleEYy0W/w5lkG2tTn/lV1uFuzr8g5z/OFfTfhz2VTxXyMGO7SNMjRlyZLUdhsKddWEIGOpOK786ipwc5PRamKMczsiVebam2TvN0vIkIU2hxDqRgLChnNU4XEekU89rbq3gSqU8jsV7oSG1HdBwD0rRdohY7mhlQ8olni4yuO3DjuAfNU3HfcVn3LR8a5c9cRHuT+LSNa0gzcAl62yURJSt6Gh3joc5nA6fEprjJVMLUVGprC+ZPw+7RfpUjmW+xaQ7wic+Go0d7A1UtacAfTXQoY+NeeSnF97asVTpOCu2WtdAqFAKAUAoBQFdcbk3b3E8dl0oUNFoGRnurFicXDDNZ4u3NalkKbnsVL9wW86o2reCpYDZ3tC2sdf8At+qubUxUpyvhvz2WvBrj5fIujBJf/TgantOF7N7bxbssDgP7j76hokjAaka+CS053ncNdazjOMpcVlfjujOtml4k6fGMSY6zzSDlBHVPQ/Cvj8VQdCtKm/d4HTpzzxTNF2xbjXC8xYUiewwz5s8O08lOHsAoC9dBoDXZ6KlOhQlUjBt3XDhxsZMSozmotkjYGZxoCmFuNBTKENpaDyVKIQN1SwBrunIA9lVdNUstRSSet3e1t9l4k8LO6tcpPKoP94W39C5/Emuh+HPZVPFfIox3aRR7IxFu3dmUdGI6jvK6qVunCUd6j3eGa6XSNRKg4cX8r7vuM+Hi3LNyId6VKdnrfmQ3ohcA3GnW1J3UABKQMjoABWjCqmqajCSlzfe9WRq5s15Kxa+T20Iu+1MXznAgRP8Aa5bh9VDbeuvtOB8atqSsiMFdnUNiGZd8vV1vgRwXtxSkFWm669ukJPihlDQ9qjXJkqlSNSdN6vRe773NKcU0pG3xrslDhl3BKg5u8FKEJzyPaPx+qubSx8U+trqzta1uW7/nIvlSb9WHiXFtmonIU4yy4hoHAUsY3j1xXUwuJWIi5RTS7+JRODi9ScOVaiAoBQCgFAKAxvHdQpW6VYGd0czUZuybtcLcoZl4hS2ww0H0PAgtq4XqLHLP1GuPWx9CsskbqXDTZmmNGcdXt4lBtOpu9xhBlPxmrqt9S7ZGcUAVrQghaD/YUnKT+dWnCuriYVOtVo3su633K6mWDSiVezc0Xa2C1LUtFyhNKEXf9d1hJxuKz/WNnsqHgD86s2OwvpMc9vXho1z/AL3XvJ0qmR24M5zf7JIgTFKmuw3FPkrDqmEgrOdc5UNa24LG061O1NNW0tfb4FdWk4y149xK2Ussl+cmZEfjMoYVhTjbCd7lqkYURyPXvFUdJY2nTpdXNN34XJYelKUsyZ55VP8Aj7af+i59aa8/Dvsqnij3HbxMGyE9LQhMx0sLdQpxtxDjobWniKHyqM+sQkYI56ac6v6RoZ3JzbSdnor7cGV0J2SSKl9MlFsbtsl1Uy4PSEKbZac4ymtCCMjPaUSNAfm61to5Z1utpxtFLla/9cyqd1HLLe5u7Nr+52z/AHOMNplXacts3RLZzvE6tRUnx9ZfcneJ0UKhiKrk8kHq/guL+neShFLVm+bOSGoFvRCtE9ictCnW5jjZyRJzlxZHPA6eAArBi5VqE4QpL1Wml3Pn7i6moTTcty9h3mA223EZbkKUOylJb1Wf/s1XR6Qw0UqUE77bEpUZu8n8y9Ty5Y8O6usjOfVegUAoBQCgFAfDighKlK0SBknwoDke1Mu3Rbq7OsF7ecZkr3pjMWY422wernESdwZ6oOpOo61mxMnFWhK0uCsnf+cycFfdaHPZT8m5XMmG6uNGQsyETiw5vurbBUFFSipSlDBIGfdUqdqMM8/Wm7Jq60v5Jd7ISvOVloi3mbTInzG57ExlmbhJW/Hiv9uSkaPAbuit0EEclJ0NHGq5qXVtNd625MknG1sx97S36JtE2l2Y3GS8GVNl1MJ/dCyU/KAFPZVkd/Wqo0asKmenTcbtN2lHW19yWaLjZv4EbZ25t7Own2EPpdQtzilS4chO7lIH4vLs1Rj8FUxk1KUGrK28SVGoqUbJmDaZ5G0L7Djr5YMdKk4RBkKznB17PgPjVuAw9TBRlGMG796I1pKrZtkKzCNapS3kzUPFSdwhUF8Edodd3vSR8a0Yjrq8Uura1v2kQgoQfa+BL2XuEHZ9b8uHIjyLmsBMaW7CfPmxUMZQjdwVHXXPh35tlUrvTqn5oiowX5iW3tA3b0yVNT0My32iiPKciyFLZC/6Racp7Ti86qPhiqYRqxvJ02293mX8sibcWu0QLK87ZLj5nOcU1HjqWy1OaQ4gpIOqQ6kghOe/OD0qNZupDrqDtJ62uvO2uvha4ho8s9jpmw8m3G4ouN8u7ouOC3Fhy5Li9wH5yVKOHCRyKdADjnmp4eSlG+bM/L4cBNa7WOoJ5VcRPaAUAoBQCgFAeEZoDXZmxVllPLeDT8ZbiitYiyFtJUo6k7qTjJPXGtVTo05u8ops9Ta2IF32Atr1vWm2oLVxQoOR5UhxbpCh807xPZUMggdDTqKeRwSsnyGZ3ucnlbKXW1Kcjpt0pjedLiWjEefShW6UncWyFApwogbwBxjSpKtWjZTjmtxTWvinbU8yR4OwXE2gXkmM4FKJK1eiZvbJBGVfJ6nJCs9SMnrXvpEv8b819Rk/7fMjuC4Q0iK9w2XJDLbIDsKW246G2yjKewCTjmRr7tK8eIaV3TdvGP1GS+l0YJ/nU2MX1SI7bL6VMB5uLKCVqKkE4VuYK8tjQa5J0qXXyX/G/OP1PMl/zfM+4ke5yZ02TEcTJWspRIQ3AlOpSQPVIDZwc9rXXOtPSZWT6t+cfqOr718SdFi3yKtpTUE/JcMJBtM3G62oqQP6PoToa89If+N+a+p7k718T7t2yV3uU6M8zbXFvR0oQ3xYrkdlJSkJSpxToClAboOEgkmoynVqxcLZU93fX3WCjGLvfU6vB8n9mYt7DC0v+cIQOLJZeW0p5fNSlbpAJJJ50lSpz0lFHqbWzLG2bJ2i2yESWWXHn2yS25JeW6UZ07O8SAfEUhThDspINt7l4NKsPD2gFAKAUAoBQCgFAMUB5igPaAhXe1QrxCXEuMdD7KsHCuaT0KTzBHQigNBa8mz4vbhdmD0ee15wjKZK86FBx2QcAAuDCiABoRms6w8NvyrZcP67iWZnQrfAiW2I3EgR248dsYQ22MAVoIkmgPMClge0AoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQH/2Q==" alt="College Logo" style="height: 100px; margin-bottom: 20px;">
    <a href="/">🏠 Home</a>
    <a href="/about">🏫 About</a>
    <a href="/results">📊 Results</a>
    <a href="/study_material">📚 Study Materials</a>
    <a href="/updates">📢 College Updates</a>
    <a href="/contact">📩 Contact</a>
    <a href="/login">🔑 Student Login</a>
    <a href="/admin">🛠 Admin</a>
</div>
"""

home_page = """<div class="section"><h1 class="title">Bachelor of Engineering College</h1><p>Your future starts here! 😊</p></div>"""
about_page = """<div class="section"><h2>🏫 About Us</h2>
    <p>Welcome to Bachelor of Engineering College, a premier institution dedicated to excellence in education and innovation. Established in 2000, we have been nurturing future engineers with state-of-the-art facilities, experienced faculty, and a vibrant campus life.</p>
    <p>Our mission is to provide a transformative learning experience that empowers students to achieve their full potential and contribute to society.</p>
</div>"""
study_material_page = """<div class="section"><h2>📚 Study Materials</h2>
    <ul>{% for sem, materials in study_materials.items() %}<li><strong>{{ sem }}:</strong>
        <ul>{% for material in materials %}<li><a href="{{ material['link'] }}" target="_blank">{{ material['name'] }}</a></li>{% endfor %}</ul>
    </li>{% endfor %}</ul>
</div>"""
updates_page = """<div class="section"><h2>📢 College Updates</h2>
    <ul>{% for update in updates %}<li class="update-item">{{ update }}
        {% if 'admin' in session %}<form method="POST" action="/remove_update" style="display: inline;">
            <input type="hidden" name="update" value="{{ update }}">
            <button type="submit">Remove</button>
        </form>{% endif %}
    </li>{% endfor %}</ul>
</div>"""
contact_page = """<div class="section"><h2>📩 Contact Us</h2>
    <form method="POST">
        <input type="text" name="name" placeholder="Your Name" required><br><br>
        <textarea name="message" placeholder="Your Message" required></textarea><br><br>
        <button type="submit" class="btn-custom">Send Message</button>
    </form>
    {% if success %}<p>{{ success }}</p>{% endif %}
</div>"""
login_page = """<div class="section"><h2>🔑 Student Login</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit" class="btn-custom">Login</button>
    </form>
    {% if error %}<p>{{ error }}</p>{% endif %}
</div>"""
admin_login_page = """<div class="section"><h2>🛠 Admin Login</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit" class="btn-custom">Login</button>
    </form>
    {% if error %}<p>{{ error }}</p>{% endif %}
</div>"""
admin_dashboard_page = """<div class="section"><h2>🛠 Admin Dashboard</h2>
    <h3>Edit Student Results</h3>
    <form method="POST" action="/edit_results">
        <select name="student" required>
            {% for student in students %}<option value="{{ student }}">{{ student }}</option>{% endfor %}
        </select><br><br>
        <select name="semester" required>
            <option value="sem1">Semester 1</option>
            <option value="sem2">Semester 2</option>
            <option value="sem3">Semester 3</option>
            <option value="sem4">Semester 4</option>
            <option value="sem5">Semester 5</option>
            <option value="sem6">Semester 6</option>
            <option value="sem7">Semester 7</option>
            <option value="sem8">Semester 8</option>
        </select><br><br>
        <input type="number" name="marks" placeholder="Marks" required><br><br>
        <button type="submit" class="btn-custom">Update Results</button>
    </form>
    <h3>Add College Update</h3>
    <form method="POST" action="/add_update">
        <textarea name="update" placeholder="New Update" required></textarea><br><br>
        <button type="submit" class="btn-custom">Add Update</button>
    </form>
    <h3>College Updates</h3>
    <ul>{% for update in updates %}<li>{{ update }}</li>{% endfor %}</ul>
    <h3>Contact Messages</h3>
    <ul>{% for message in messages %}<li><strong>{{ message['name'] }}:</strong> {{ message['message'] }}</li>{% endfor %}</ul>
    <h3>Admin Logs</h3>
    <div class="logs">{% for log in logs %}<div class="log"><strong>{{ log['timestamp'] }}:</strong> {{ log['action'] }}</div>{% endfor %}</div>
    <a href="/admin_logout" class="btn-custom">🚪 Admin Logout</a>
    <a href="/" class="btn-home">🏠 Home</a>
</div>"""
semester_selection_page = """<div class="section"><h2>📊 Select Semester</h2>
    <form method="POST">
        <select name="semester" required>
            <option value="sem1">Semester 1</option>
            <option value="sem2">Semester 2</option>
            <option value="sem3">Semester 3</option>
            <option value="sem4">Semester 4</option>
            <option value="sem5">Semester 5</option>
            <option value="sem6">Semester 6</option>
            <option value="sem7">Semester 7</option>
            <option value="sem8">Semester 8</option>
        </select><br><br>
        <button type="submit" class="btn-custom">View Results</button>
    </form>
    <a href="/" class="btn-home">🏠 Home</a>
</div>"""
results_page = """<div class="section"><h2>📊 Results</h2>
    <p>Hello, {{ username }}!</p>
    <p>Your marks for {{ semester }}: {{ marks }}</p>
    <p>Your SGPA: {{ sgpa }}</p>
    <a href="/" class="btn-home">🏠 Home</a>
</div>"""

# 🏠 **Home Page**
@app.route('/')
def home():
    return render_template_string(css_styles + nav_bar + home_page)

# 📌 **About Us Page**
@app.route('/about')
def about():
    return render_template_string(css_styles + nav_bar + about_page)

# 📊 **Results Page**
@app.route('/results', methods=['GET', 'POST'])
def results():
    if 'username' in session:
        student = session['username']
        if request.method == 'POST':
            semester = request.form['semester']
            if semester in students[student]['results']:
                marks = students[student]['results'][semester]
                sgpa = round(marks / 10, 2)
                return render_template_string(css_styles + nav_bar + results_page, username=student, marks=marks, sgpa=sgpa, semester=semester)
        return render_template_string(css_styles + nav_bar + semester_selection_page, username=student)
    return redirect(url_for('login'))

# 📚 **Study Materials Page**
@app.route('/study_material')
def study_material():
    return render_template_string(css_styles + nav_bar + study_material_page, study_materials=study_materials)

# 📢 **College Updates Page**
@app.route('/updates')
def updates():
    return render_template_string(css_styles + nav_bar + updates_page, updates=college_updates)

# 📩 **Contact Us Page**
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        contact_messages.append({"name": name, "message": message})
        return render_template_string(css_styles + nav_bar + contact_page, success="✅ Message Sent Successfully!")
    return render_template_string(css_styles + nav_bar + contact_page, success=None)

# 🔑 **Login Page**
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in students and students[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('results'))
        return render_template_string(css_styles + nav_bar + login_page, error="❌ Invalid credentials! Try again.")
    return render_template_string(css_styles + nav_bar + login_page, error=None)

# 🚪 **Logout**
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# 🔑 **Admin Login**
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in admin_credentials and admin_credentials[username] == password:
            session['admin'] = username
            admin_logs.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": f"Admin {username} logged in."})
            return redirect(url_for('admin_dashboard'))
        return render_template_string(css_styles + nav_bar + admin_login_page, error="❌ Invalid Admin Credentials!")
    return render_template_string(css_styles + nav_bar + admin_login_page, error=None)

# 🔧 **Admin Dashboard**
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    return render_template_string(css_styles + nav_bar + admin_dashboard_page, students=students, updates=college_updates, messages=contact_messages, logs=admin_logs)

# ✏️ **Edit Student Results**
@app.route('/edit_results', methods=['POST'])
def edit_results():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    student = request.form['student']
    semester = request.form['semester']
    marks = int(request.form['marks'])
    students[student]['results'][semester] = marks
    admin_logs.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": f"Admin {session['admin']} updated {student}'s {semester} marks to {marks}."})
    return redirect(url_for('admin_dashboard'))

# 📝 **Add College Update**
@app.route('/add_update', methods=['POST'])
def add_update():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    update = request.form['update']
    college_updates.append(update)
    admin_logs.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": f"Admin {session['admin']} added a new update: {update}."})
    return redirect(url_for('admin_dashboard'))

# 🗑️ **Remove College Update**
@app.route('/remove_update', methods=['POST'])
def remove_update():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    update = request.form['update']
    if update in college_updates:
        college_updates.remove(update)
        admin_logs.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": f"Admin {session['admin']} removed update: {update}."})
    return redirect(url_for('admin_dashboard'))

# 🚪 **Admin Logout**
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True) 
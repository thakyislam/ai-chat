from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from django.conf import settings
from google import genai
import anthropic

# Create your views here.

@login_required
def home(request):
    if request.method == "POST":
        prompt = request.POST.get('prompt')
        task_type = request.POST.get('task_type')
        ai_response_text = "This is a dummy response"
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt,
        )
        ai_response_text = response.text
    else:
        ai_response_text = None
    return render(request, 'core/home.html', {'response': ai_response_text})

@require_GET
def logout_view(request):
    logout(request)
    return redirect('login')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def dress_suggestion(request):
    suggestion = None
    error = None
    event_description = ""

    if request.method == "POST":
        event_description = request.POST.get('event_description', '').strip()
        if event_description:
            try:
                client = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)
                with client.messages.stream(
                    model="claude-opus-4-6",
                    max_tokens=1024,
                    system=(
                        "You are a personal fashion stylist. "
                        "Given a description of a function or event, suggest appropriate outfits to wear. "
                        "Be specific about clothing items, colors, and accessories. "
                        "Keep suggestions practical and considerate of the event's formality level."
                    ),
                    messages=[
                        {
                            "role": "user",
                            "content": f"What should I wear to this event? {event_description}"
                        }
                    ],
                ) as stream:
                    suggestion = stream.get_final_message().content[0].text
            except anthropic.AuthenticationError:
                error = "Invalid API key. Check CLAUDE_API_KEY in your .env file."
            except anthropic.APIConnectionError:
                error = "Could not connect to Claude API. Check your internet connection."
            except anthropic.APIStatusError as e:
                error = f"API error ({e.status_code}): {e.message}"
        else:
            error = "Please describe your event or function."

    return render(request, 'core/dress_suggestion.html', {
        'suggestion': suggestion,
        'error': error,
        'event_description': event_description,
    })
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from google import genai
import certifi
import os

from .models import PromptRequest, PromptResponse


@login_required
def home(request):
    prompt = ""
    task_type = ""

    if request.method == "POST":
        prompt = request.POST.get('prompt')
        task_type = request.POST.get('task_type')

        ai_response_text = "This is a dummy response"
        os.environ['SSL_CERT_FILE'] = certifi.where()
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-3-flash-preview",  # your original model
            contents=prompt,
        )
        ai_response_text = response.text

        # Save to DB
        prompt_obj = PromptRequest.objects.create(
            user=request.user,
            task_type=task_type,
            prompt_text=prompt,
        )
        PromptResponse.objects.create(
            request=prompt_obj,
            model_name="gemini-3-flash-preview",
            response_text=ai_response_text,
        )
    else:
        ai_response_text = None

    # Sidebar history
    prompts = PromptRequest.objects.filter(user=request.user).select_related('response')[:20]

    context = {
        'response': ai_response_text,
        'prompt': prompt,
        'task_type': task_type,
        'prompts': prompts,
    }
    return render(request, 'core/home.html', context)


@login_required
def prompt_detail(request, prompt_id):
    selected = get_object_or_404(PromptRequest, id=prompt_id, user=request.user)
    prompts = PromptRequest.objects.filter(user=request.user).select_related('response')[:20]

    context = {
        'selected_prompt': selected,
        'prompts': prompts,
        'response': selected.response.response_text if hasattr(selected, 'response') else None,
        'prompt': selected.prompt_text,
        'task_type': selected.task_type,
    }
    return render(request, 'core/home.html', context)


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
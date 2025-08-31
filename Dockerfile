FROM python:3

RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

COPY --chown=user ./requirements.txt .

WORKDIR /api

RUN pip install --upgrade pip
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p dump models static templates

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
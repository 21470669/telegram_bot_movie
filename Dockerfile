FROM python
COPY chatbot.py /
COPY requirements.txt / 
RUN pip install pip update
RUN pip install awslambdaric
RUN pip install -r requirements.txt
ENV ACCESS_TOKEN=5214558166:AAEqXN0GDUMLA9ynkDNnASbIN5JUzUreBmo
ENV TMDB_KEY=3471e2b3afebbefa68e2f08ec2d9092a
#ENV HOST="redis-10618.c270.us-east-1-3.ec2.cloud.redislabs.com"
#ENV PASSWORD="hm7fsUzgPvONxmnpzaVqNHQ3nuMJlYpR"
#ENV REDISPORT=10618  
ENV client_link="mongodb+srv://comp7940group27:my_password@cluster0.rz17h.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
CMD python chatbot.py
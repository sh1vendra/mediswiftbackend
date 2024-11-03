Shivendra
shiv_endra_007
Online



A wild limontan appeared. — Yesterday at 1:24 PM
Shivendra — Yesterday at 1:25 PM
Hi everybody
Shivendra — Yesterday at 1:25 PM
Anish just landed. — Yesterday at 1:26 PM
Welcome Nirman Khadka. Say hi! — Yesterday at 1:27 PM
Shivendra — Today at 7:25 AM
BuVpxqyXUjzIFrqTksxPQvowfUbLOLSL
postgresql://postgres:BuVpxqyXUjzIFrqTksxPQvowfUbLOLSL@postgres.railway.internal:5432/railway
postgresql://postgres:BuVpxqyXUjzIFrqTksxPQvowfUbLOLSL@junction.proxy.rlwy.net:54509/railway
Nirman Khadka — Today at 8:01 AM
helper>base_api.js
"
import axios from 'axios';

const axiosInstance = axios.create({
    // baseURL: "https://mediswiftserver.azurewebsites.net/api/",
    baseURL: "http://localhost:8000/api/",
});

export default axiosInstance;
"
chatThread.js:
"
"use client";
import { useState, useEffect } from 'react';
import HumanResponse from './HumanResponse';
import BotResponse from './BotResponse';
Expand
message.txt
3 KB
prompt.js
"
"use client";

import { useState, useRef } from 'react';
import Image from 'next/image';
Expand
message.txt
4 KB
Shivendra — Today at 8:07 AM
http://mediswiftbackend-production.up.railway.app/
Nirman Khadka — Today at 8:19 AM
# Install required libraries (uncomment if running for the first time)
!pip install transformers torch bitsandbytes kagglehub peft

# Import necessary libraries
import kagglehub
import pandas as pd
Expand
message.txt
7 KB
Anish — Today at 8:22 AM
Since there is no prior chat history and no treatment data found, we need to start gathering information. To proceed, I'd like to ask some questions. Could you please tell me what brings you here today? What seems to be the issue or concern you're experiencing?
fsadfdf
human
bot
Existing treatment data not found. Since no meaningful context or information was provided in the question "fsadfdf", we cannot determine the required treatment data. Please provide a clear description of the issue or concern you are experiencing so we can gather the necessary information to proceed with the patient's case.
ok
Expand
message.txt
5 KB
Nirman Khadka — Today at 8:26 AM
import json
from datetime import datetime
from v01.models import Query, Treatment
from groq import Groq
from rest_framework.response import Response
from rest_framework import status
Expand
message.txt
6 KB
Anish — Today at 8:30 AM
https://github.com/anishrajpandey/mediswift
GitHub
GitHub - anishrajpandey/mediswift
Contribute to anishrajpandey/mediswift development by creating an account on GitHub.
GitHub - anishrajpandey/mediswift
Nirman Khadka — Today at 8:44 AM
"use client";

import React, { useState, useEffect } from "react";
import axiosInstance from "./axiosInstance"; // Make sure axiosInstance is correctly configured
import Navbar from "./Navbar";
Expand
message.txt
4 KB
Nirman Khadka — Today at 9:02 AM
"use client";

import React, { useState, useEffect } from "react";
import axiosInstance from "./axiosInstance";
import Navbar from "./Navbar";
Expand
message.txt
7 KB
Nirman Khadka — Today at 9:40 AM
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action

from v01.utility import create_response, process_patient_query
Expand
message.txt
4 KB
﻿
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action

from v01.utility import create_response, process_patient_query
from .models import Query, Treatment
from .serializers import QuerySerializer, TreatmentSerializer

class QueryViewSet(viewsets.ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

    @action(detail=False, methods=['post'])
    def process_chat(self, request):
        """
        Process a chat query and generate a response.
        """
        query_text = request.data.get('query')
        if not query_text:
            raise ValidationError('Query text is required')
        
        try:
            # Process the query and create a response
            response_text = process_patient_query(query_text)
            query = Query.objects.create(query_text=query_text, response_text=response_text)
            
            return create_response(
                success=True,
                message='Query processed successfully',
                body=QuerySerializer(query).data,
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            return create_response(
                success=False,
                message=f'Error processing query: {str(e)}',
                status=status.HTTP_400_BAD_REQUEST
            )
        
    @action(detail=False, methods=['get'])
    # delete all the queries
    def delete_all(self, request):
        """
        Delete all queries.
        """
        try:
            Query.objects.all().delete()
            return create_response(
                success=True,
                message='All queries deleted successfully',
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return create_response(
                success=False,
                message=f'Error deleting queries: {str(e)}',
                status=status.HTTP_400_BAD_REQUEST
            )

class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

    @action(detail=True, methods=['put'])
    def change_status(self, request, pk=None):
        """
        Change the status of a treatment instance.
        """
        try:
            treatment = Treatment.objects.get(pk=pk)
            new_status = request.data.get('status')
            treatment.status = new_status
            treatment.save()
            
            return create_response(
                success=True,
                message='Treatment status updated successfully',
                body=TreatmentSerializer(treatment).data,
                status=status.HTTP_200_OK
            )
        
        except ObjectDoesNotExist:
            return create_response(
                success=False,
                message='Treatment not found',
                status=status.HTTP_404_NOT_FOUND
            )
        
        except Exception as e:
            return create_response(
                success=False,
                message=f'Error updating treatment status: {str(e)}',
                status=status.HTTP_400_BAD_REQUEST
            )
        
    @action(detail=False, methods=['get'])
    # delete all the treatments
    def delete_all(self, request):
        """
        Delete all treatments.
        """
        try:
            Treatment.objects.all().delete()
            return create_response(
                success=True,
                message='All treatments deleted successfully',
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return create_response(
                success=False,
                message=f'Error deleting treatments: {str(e)}',
                status=status.HTTP_400_BAD_REQUEST
            )
message.txt
4 KB
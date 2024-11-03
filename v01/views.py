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
